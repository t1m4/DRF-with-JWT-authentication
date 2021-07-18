import datetime


def get_object_or_none(klass, *args, **kwargs):
    try:
        return klass._default_manager.get(*args, **kwargs)
    except klass.DoesNotExist:
        return None


def from_date_to_datetime(date):
    """
    Convert date to datetime object
    """
    return datetime.datetime(date.year, date.month, date.day)

def datetime_format(date_and_time):
    return date_and_time.strftime("%Y-%m-%d %H:%M:%S")