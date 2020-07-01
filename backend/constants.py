import string


# total combination: (26*2+10) ** 5 = 916,132,832  > 10,000,000
BASIC_CHAR = ''.join([
    string.ascii_uppercase,
    string.ascii_lowercase,
    string.digits
])

SHORT_PATH_LEN = 5
