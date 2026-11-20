import datetime

def current_time():
    return str(datetime.datetime.now())

def current_date():
    return str(datetime.date.today().isoformat())