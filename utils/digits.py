"""Utility functions for extracting and converting digit sequences between bases."""

import numpy as np
from mpmath import mpf

def get_nb_digits_base_10(base: int, nb_digits: int) -> int:
    """
    Compute the number of base-10 digits needed to obtain `nb_digits` digits in a given base.

    Parameters
    ----------
    base : int
        Radix base to convert to.
    nb_digits : int
        Number of digits desired in the target base.

    Returns
    -------
    nb_digits_base_10 : int
        Number of base-10 digits required.
    """
    return int(np.ceil(nb_digits * np.log10(base)))


def get_digits_in_base(x: mpf, base: int, nb_digits: int) -> np.ndarray:  # type: ignore
    """
    Extract the first `nb_digits` digits of `x` in base `base`, after conversion if needed.

    Parameters
    ----------
    x : mpmath.mpf
        Number in base 10.
    base : int
        Radix base to convert to.
    nb_digits : int
        Number of digits to extract.

    Returns
    -------
    digits : ndarray of int
        Array of digits in the specified base.
    """
    if base == 10:
        # no conversion needed, just get the 10-digits, but restore the possible
        # trailing 0s that were dropped in 'x'
        digits = np.array([int(d) for d in str(x).split('.')[1]])
        digits = np.pad(digits, (0, nb_digits-len(digits)), mode="constant", constant_values=0)
    else:
        # convert x and store the b-digits
        x -= int(x)
        digits = np.zeros(nb_digits, dtype=int)
        for i in range(nb_digits):
            x *= base
            digit = int(x)
            digits[i] = digit
            x -= digit

    return digits
