import unittest, requests


class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/"
    PARK_CAR = "{}/parkcar".format(API_URL)
    CAR_OBJ = {
        "car_number": "RD19"
    }

    def test_1_get_parking_space(self):
        r = requests.get(self.API_URL)
        self.assertEqual(r.status_code, 200)

    def test_2_park_car(self):
        r = requests.post(ApiTest.PARK_CAR, json=ApiTest.CAR_OBJ)
        self.assertEqual(r.status_code, 200)
        print(r.text)
        self.assertNotEqual("Parking Space is full", r.text)

