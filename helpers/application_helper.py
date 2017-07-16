"""
# Application Helpers
"""
#
# Miscellaneous
#
def parameterize(value):
    value = value.strip().lower()
    value = value.replace(' ', '-')
    return value

def pluralize(seq_or_int, singular = '', plural = 's'):
    if type(seq_or_int) == int:
        number = seq_or_int
    else:
        number = len(seq_or_int)

    if number == 1:
        return singular
    else:
        return plural

def if_none(value, default=''):
    if value is not None:
        return value
    else:
        return default

def zero_positive_negative(value):
    if value > 0:
        return 'positive'
    elif value < 0:
        return 'negative'
    else:
        return 'zero'

def at(a_datetime):
    f = '%Y-%m-%d %H:%M:%S'

    if not a_datetime:
        return 'N/A'
    else:
        return a_datetime.strftime(f).lower()
