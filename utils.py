from datetime import datetime, timezone, time
from typing import Optional

def to_utc(datetime_str: str) -> datetime:
    """
    Precondition: datetime_str is in proper strptime format
    """
    return datetime.strptime(datetime_str, "%d/%m/%y %H:%M")



