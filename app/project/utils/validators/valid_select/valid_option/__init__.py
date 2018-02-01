from re import match

def valid_option(option: str, options: list) -> bool:
    """Take an <option> value and verify that it exists in the supplied
       list of options. (Value may require type conversion.)
    """
    if answer.answer in selectoptions:
        return True
    else:
        # check for string->int conversion
        if match(r'^\d+$', answer.answer) and type(selectoptions[0]) is int:
            return int(answer.answer) in selectoptions
        else:
            return False
