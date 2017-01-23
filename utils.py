import datetime


def working_hours():
    d = datetime.datetime.now()
    if d.hour < 21 or d.hour >= 23:
        return False
    return True
