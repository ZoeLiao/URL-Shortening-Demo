import random
import string

from shortener.models import URL


# total combination: (24*2+10) ** 5 = 656,356,768  > 10,000,000
BASIC_CHAR = ''.join([
    string.ascii_uppercase,
    string.ascii_lowercase,
    string.digits
])
SHORTEN_URL_LEN = 5


def create_short_path():
    short_path = ''.join(
        random.choice(BASIC_CHAR) for _ in range(SHORTEN_URL_LEN)
    )
    while URL.objects.filter(short_path=short_path).exists():
        short_path = ''.join(
            random.choice(BASIC_CHAR) for _ in range(SHORTEN_URL_LEN)
        )
    return short_path


def get_short_url(request, short_path):
    schema = request.scheme
    host = request.get_host()
    return f'{schema}://{host}/shortener/{short_path}'
