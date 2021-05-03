from flask import render_template, request, jsonify, abort, Response
from app import app
from app.models import RateLimiter
from dotenv import load_dotenv

import os

load_dotenv()
limiter = RateLimiter

PARKING_SIZE = os.getenv("PARKING_LOT_SIZE")
PARKING_SPACE = dict.fromkeys(range(int(PARKING_SIZE)))


# function to check if the parking space is full
def is_parking_full():
    assert None in PARKING_SPACE.values(), "parking space is full"


# function to check the request method
def check_method(request):
    if request.method == 'POST':
        return request.json


# function to check whether the slot_number from the request is a valid input
def check_for_valid_slot(slot):
    try:
        valid = int(slot)
        assert valid > 0, "Invalid slot number"
    except (ValueError, AssertionError):
        abort(Response("Enter a valid slot number"))
    return valid


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return jsonify({"Parking Space": PARKING_SPACE})


@app.route('/parkcar', methods=['POST'])
@limiter(calls=10, period=10)
def park_a_car():
    req_Json = check_method(request)
    car_number = req_Json['car_number']
    parked_slot = -1

    try:
        is_parking_full()
    except AssertionError:
        abort(Response("Parking Space is full"))

    for slot, car in PARKING_SPACE.items():
        if car is None:
            PARKING_SPACE[slot] = car_number
            parked_slot = slot
            break
    return Response("Your car is parked at slot: " + str(parked_slot))


@app.route('/unparkcar', methods=['POST'])
def unpark_your_car():
    req_Json = check_method(request)
    slot_number = check_for_valid_slot(req_Json['slot_number'])

    if slot_number < int(PARKING_SIZE):
        if PARKING_SPACE[slot_number] is not None:
            PARKING_SPACE[slot_number] = None
            return Response("Slot number " + str(slot_number) + " has been freed")
        else:
            return Response("The slot " + str(slot_number) + " is empty")
    return Response("The slot number exceeds the Parking space size. The Parking space size is: " + PARKING_SIZE)


@app.route('/getcarslotinfo', methods=['POST'])
def get_car_slot_info():
    req_Json = check_method(request)
    # Car number sent in the request.
    if 'car_number' in req_Json:
        car_number = req_Json['car_number']
        for slot, car in PARKING_SPACE.items():
            if car == car_number:
                return Response("Car number " + car_number + " is present at slot " + str(slot))
        return Response("Car number " + car_number + "is not present in this parking space. Please try to remember "
                                                     "your car number")

    # Slot number sent in the request.
    elif 'slot_number' in req_Json:
        slot = req_Json['slot_number']
        check_for_valid_slot(slot)
        car_number = PARKING_SPACE.get(slot)

        if car_number is not None:
            return Response("Car number " + car_number + " is present at slot " + slot)
        else:
            return Response("The slot " + slot + " is empty")
