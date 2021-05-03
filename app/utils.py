import time


def now():
    if hasattr(time, 'monotonic'):
        return time.monotonic
    return time.time
