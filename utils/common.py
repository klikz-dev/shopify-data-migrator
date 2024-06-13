import re
from datetime import datetime


def to_text(text):
    if (isinstance(text, int) or isinstance(text, float)) and text.is_integer():
        return int(text)

    if text:
        text = re.sub(r'[^\x20-\x7E]+', '', str(text))
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    else:
        return ""


def to_float(value):
    if value:
        try:
            value = round(float(to_text(value)), 2)
        except:
            value = 0
    else:
        value = 0

    if value == int(value):
        return int(value)
    else:
        return value


def to_int(value):
    return int(to_float(value))


def to_date(value):
    try:
        date = datetime.strptime(
            value, "%m/%d/%Y").date() if value else None
        return date
    except:
        return None


def to_handle(text):
    if text:
        handle = str(text).lower().replace(" ", "-")
        handle = re.sub(r'[^a-z0-9-]', '', handle)
        handle = re.sub(r'-+', '-', handle)

        return handle.strip('-')
    else:
        return ""
