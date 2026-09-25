import random
import string
from datetime import datetime, timedelta, timezone
from typing import Tuple


def generate_random_string(length: int = 8, chars: str = string.ascii_letters) -> str:
    return "".join(random.choices(chars, k=length))


def generate_password(length: int) -> str:
    return generate_random_string(
        length=length, chars=string.ascii_letters + string.digits
    )


def generate_email(length: int, chars: str = string.ascii_letters) -> str:
    return generate_random_string(length=length, chars=chars) + "@mail.com"


def generate_isoformat_range() -> Tuple[str, str]:
    start = (datetime.now() - timedelta(days=7)).isoformat(timespec="seconds")
    end = datetime.now().isoformat(timespec="seconds")
    return start, end

def generate_date_range() -> tuple[str, str]:
    """Generate date range in YYYY-MM-DD format for the past 7 days"""
    end = datetime.now()
    start = end - timedelta(days=7)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def generate_utc_isoformat_range() -> Tuple[str, str]:
    """Timezone-aware ISO range: endpoints such as /system/stats/digest reject a naive datetime."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)
    return (
        start.isoformat(timespec="seconds"),
        end.isoformat(timespec="seconds"),
    )
