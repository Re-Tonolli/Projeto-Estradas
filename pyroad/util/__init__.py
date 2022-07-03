from math import floor


def format_zeros(value):
    try:
        return int(value) if value == floor(value) else value
    except:
        return value


def round_values(value):
    from pyroad.util.Angulo import Angulo
    try:
        return round(value, Angulo.DEC_PLACES)
    except:
        return value
