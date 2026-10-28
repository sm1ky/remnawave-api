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


def generate_unroutable_address() -> str:
    """Адрес для тестовых нод и хостов: заведомо нерабочий, но почти всегда уникальный.

    Первый октет заведомо больше 255, так что адрес никуда не резолвится и
    подключения не будет. Прежний вариант `randint(500, 800)` + `.0.0.1` давал
    всего 301 значение, а адрес ноды на панели уникален — отсюда случайные
    ConflictError на повторных прогонах.
    """
    return (
        f"{random.randint(500, 999)}"
        f".{random.randint(0, 255)}"
        f".{random.randint(0, 255)}"
        f".{random.randint(1, 254)}"
    )
