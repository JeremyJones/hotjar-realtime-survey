def valid_option(option: str, options: list) -> bool:
    """Take an <option> value and verify that it exists in the supplied
       list of options. (Value may require type conversion.)
    """
    if option in options:
        return True
    elif len(options) and type(options[0]) is int:
        try:
            return int(option) in options
        except Exception:
            pass
        
    return False
