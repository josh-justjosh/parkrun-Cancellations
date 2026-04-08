import datetime
from zoneinfo import ZoneInfo


def now():
    '''returns the current datetime'''
    return datetime.datetime.now()


def same_week(date_string):
    '''True if date_string (YYYY-MM-DD) is in the same ISO week as now in Europe/Dublin.'''
    tz = ZoneInfo('Europe/Dublin')
    d1 = datetime.datetime.strptime(date_string, '%Y-%m-%d').replace(tzinfo=tz)
    d2 = datetime.datetime.now(tz)
    return d1.isocalendar()[:2] == d2.isocalendar()[:2]
