import datetime as date

from time import strftime
from requests_html import HTMLSession
from datetime import datetime, timezone

def convert_time(times: str) -> int:
    dt = date.datetime.fromisoformat(times)
    dt = dt.replace(tzinfo=timezone.utc) 

    return int(dt.timestamp())
    ...

def now():
    return strftime('%Y-%m-%d %H:%M:%S')
    ...

def today():
    return datetime.now().strftime("%Y-%m-%d")
    ...

def change_format(dates: str) -> str:
    try: return dates.replace('T', ' ')
    except Exception: return dates