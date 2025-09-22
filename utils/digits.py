""" TODO """

import numpy as np

def get_nb_digits_base_10(base, nb_digits):
    """Compute the number of base-10 digits needed to get 'nb_digits' digits in base 'base'."""
    return int(np.ceil(nb_digits * np.log10(base)))


def get_digits_in_base(x, base, nb_digits):
    """Return the nb_digits of x in base 'base', after conversion if needed."""
    if base == 10:
        # no conversion needed, just get the 10-digits, but restore the possible
        # trailing 0s that were dropped in 'x'
        result = np.array([int(d) for d in str(x).split('.')[1]])
        result = np.pad(result, (0, nb_digits-len(result)), mode="constant", constant_values=0)
    else:
        # convert x and store the b-digits
        x -= int(x)
        result = np.zeros(nb_digits, dtype=int)
        for i in range(nb_digits):
            x *= base
            digit = int(x)
            result[i] = digit
            x -= digit

    return result
