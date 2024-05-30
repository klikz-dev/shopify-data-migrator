import re


def toText(text):
    if text:
        text = re.sub(r'[^\x20-\x7E]+', '', str(text))
        text = re.sub(r'\s+', ' ', text)
        return text
    else:
        return ""


def toFloat(value):
    if value:
        try:
            value = round(float(toText(value)), 2)
        except:
            value = 0
    else:
        value = 0

    if value == int(value):
        return int(value)
    else:
        return value


def toInt(value):
    return int(toFloat(value))


def toHandle(text):
    if text:
        handle = str(text).lower().replace(" ", "-")
        handle = re.sub(r'[^a-z0-9-]', '', handle)
        handle = re.sub(r'-+', '-', handle)

        return handle.strip('-')
    else:
        return ""
