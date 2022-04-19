"""utility functions"""

from datetime import datetime


def convert_to_time(f: str or dict):
    """
    Converts argument to a time object.

    :param f: str | dict, object containing date components
    :return: time object
    """

    if f is None:
        return None

    if isinstance(f, dict):
        year = f.get('year')
        month = f.get('month')
        day = f.get('day')
        if year and month:
            date = '{year}-{month:02}'.format(year=year, month=month)
            if day:
                date += '-{day:02}'.format(day=day)
        elif year:
            date = str(year)
        else:
            return None
        f = date

    if f.count('-') == 2:
        date_format = "%Y-%m-%d"
    elif f.count('-') == 1:
        date_format = "%Y-%m"
    elif ',' in f:
        date_format = "%B %d, %Y"
    elif f.isdigit():
        date_format = "%Y"
    else:
        date_format = "%B %Y"

    return datetime.strptime(f, date_format)
