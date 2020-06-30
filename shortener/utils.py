import random

from backend.constants import (
    BASIC_CHAR,
    SHORT_PATH_LEN,
)
from shortener.models import URL


def create_short_path():
    short_path = _create_short_path()
    while URL.objects.filter(short_path=short_path).exists():
        short_path = _create_short_path()
    return short_path


def _create_short_path():
    return ''.join(
        random.choice(BASIC_CHAR) for _ in range(SHORT_PATH_LEN)
    )


def get_short_url(request, short_path):
    schema = request.scheme
    host = request.get_host()
    return f'{schema}://{host}/{short_path}'
