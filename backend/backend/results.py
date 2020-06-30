from collections import namedtuple
from functools import partial


DEFAULT_CODE_LEN = 4

Result = namedtuple('Result', ['code', 'msg', 'detail'])

# result type
SUCCESS = Result('0'*DEFAULT_CODE_LEN, 'Success', '')
DB_ERROR = partial(
    Result,
    ''.join(['1', '0'*(DEFAULT_CODE_LEN-1)]),
    'DB Error'
)
REQUEST_ERROR = partial(
    Result,
    ''.join(['2', '0'*(DEFAULT_CODE_LEN-1)]),
    'Request Error'
)
