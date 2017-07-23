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
