from json import loads as loadjson
from .valid_option import valid_option

def valid_select(answer:str, options_json) -> bool:
    """For a question which requires an answer chosen from a <select>
    input, validate the answer.
    """
    if not options_json:   # if we have no options then we just check the string
        return valid_string(answer)
    
    selectoptions:list = loadjson(options_json)

    if not len(selectoptions):
        return False

    return valid_option(answer, selectoptions)
