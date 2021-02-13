def cast_boolean(val):
    val = str(val)
    return False if val == "" else bool(_strtobool(val))
