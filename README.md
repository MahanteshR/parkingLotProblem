## Take Home Test 

###### BACKEND - Implementing a Flask server.
###### *Owner* - Mahantesh.R

### Installation

Execute the requirements.txt file
```
    > pip install -r requirements.txt 
```

### Usage
The project directory consists of `app` package. The directory structure is as follows:
```html
takeHomeTest
├───app
│   ├───__init__.py
│   ├───models.py
│   ├───routes.py
│   └───utils.py
├───.env
├───main.py
├───README.md
└───requirements.txt
```
The *routes* file has all the endpoints and *models* has the `RateLimiter`  class defined.

To run the application, from the root directory, execute:
```
    > python main.py
```

In *routes.py*, the `PARKING_SPACE` dictionary as the name suggests is our parking space 
and holds key-value pairs with *parking slots as keys(int)* and *car numbers as values(string)*.

The `PARKING_SIZE` variable is fetched from `.env` file. Once it's value is changed
in the `.env` file, the application has to be rerun again.

There are 4 main API Endpoints:
* endpoint -  ```http://127.0.0.1:5000/```
    *  `GET` request to this URL, fetches the parking space details, by default all the 
    slots hold None, indicating no car is parked at that respective slot.
       

* endpoint - ```http://127.0.0.1:5000/parkcar```
    * `POST` request to this URL with `car_number` specified in the body of the request
    maps a parking slot to the respective car number. The mappings happen from the beginning of the
      dictionary, if the slot is `None`, then it is mapped to a car number respectively.
      
    ```
    {
    "car_number" : "RD19"
    }
    ```
  *   When the parking space is full, the appropriate response is sent.
  * The API call *rate limits* to 10 requests made within a time window 
    of 10 sec. The `RateLimiter` decorator defined in *models.py* checks the number 
    of calls made for a specified window rate. When a request is made, it checks 
    for the remaining time window, if there's space for requests to accommodated,
    it allows the forthcoming requests to happen. If the number of successive calls made
    increases the specified calls within that time frame, an appropriate response is sent back to
    the user.  
  *  The decorator function takes 3 parameters:
        * calls - the maximum number of calls.
        * period - time window in seconds.
        * clock(optional) - to get the current time.
    ```
    from app.models import RateLimiter
    limiter = RateLimiter
    @limiter(calls=10, period=10)
    ```
  
  
* endpoint - ```http://127.0.0.1:5000/unparkcar```
    * `POST` request to this URL with `slot_number` specified in the body of the request
    frees the parking slot if occupied by a car number.
  ```
    {
    "slot_number" : "2"
    }
    ```
      
      
* endpoint - ```http://127.0.0.1:5000/getcarslotinfo```
    * `POST` request to this URL with `slot_number` or `car_number` specified in the body 
      of the request will fetch the respective slot-car details.
      
---
###### NOTE

All error handling cases are handled wherever possible. For example, 
handling cases where a negative slot number is entered and so on.`
--- 

#### References
* Flask - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
* Rate Limiter - https://github.com/tomasbasham/ratelimit