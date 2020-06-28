import string


# total combination: (24*2+10) ** 5 = 656,356,768  > 10,000,000
BASIC_CHAR = ''.join([
    string.ascii_uppercase,
    string.ascii_lowercase,
    string.digits
])

SHORT_PATH_LEN = 5
