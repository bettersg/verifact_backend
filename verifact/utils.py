def _strtobool(val):
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise valError("invalid truth val %r" % (val,))

def cast_boolean(val):
    if val == False:
        return False
    val = str(val)
    return False if val == "" else bool(_strtobool(val))
