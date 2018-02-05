from re import match

def valid_string(check_str: str) -> bool:
    """Check whether a string adheres to our rules. Currently non-zero length.
    """
    return len(check_str) > 0 and match(r'[a-zA-Z0-9]', check_str)
