import sys
from functools import wraps
from math import floor
from flask import Response
from app.utils import now

import threading


class RateLimiter(object):

    def __init__(self, calls=10, period=10, clock=now()):
        self.calls = max(1, min(sys.maxsize, floor(calls)))
        self.period = period
        self.clock = clock

        self.last_check = clock()
        self.calls_made = 0

        self.lock = threading.RLock()

    def __call__(self, func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            with self.lock:
                period_remaining = self.__period_remaining()

                if period_remaining <= 0:
                    self.calls_made = 0
                    self.last_check = self.clock()

                self.calls_made += 1
                # print("calls made", self.calls_made)

                if self.calls_made > self.calls:
                    return Response("Only 10 requests are allowed within a 10 sec time window, please try "
                                    "again after a few seconds.")

            return func(*args, **kwargs)

        return wrapper_func

    def __period_remaining(self):
        elapsed_time = self.clock() - self.last_check
        return self.period - elapsed_time
