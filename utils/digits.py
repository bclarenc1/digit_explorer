# pylint: disable=unnecessary-lambda-assignment

"""Utility functions for extracting and converting digit sequences between bases."""

import numpy as np
from mpmath import mpf

def get_nb_digits_base_10(base: int, nb_digits: int) -> int:
    """
    Compute the number of base-10 digits needed to obtain ``nb_digits`` digits in a given base.

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
    Extract the first ``nb_digits`` digits of ``x`` in base ``base``, after conversion if needed.

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


def format_digit_sequence(digit_sequence: list[int], base: int, nb_digits_per_row: int = 100) -> str:
    """
    Format a sequence of digits into a string block with aligned rows.

    The digits are grouped into rows of fixed length, with formatting adapted to the numeric base.
    For bases ≤ 10, digits are printed contiguously without separators.
    For bases > 10, digits are right-aligned and separated by spaces to avoid ambiguity.

    Parameters
    ----------
    digit_sequence : list of int
        List of digits to format. Each digit must be in the range [0, base).
    base : int
        Numeric base used to interpret the digits. Must be greater than 1.
    nb_digits_per_row : int, optional
        Number of digits per row in the output block (default is 100).

    Returns
    -------
    sequence_block : str
        A string containing the formatted digit sequence, split into rows.
    """
    if base <= 10:
        # print digits contiguously
        formatter = str
        sep = ""
    else:
        # separate and align digits
        nb_chars_per_digits = int(np.ceil(np.log10(base)))
        formatter = lambda d: f"{d:>{nb_chars_per_digits}d}"
        sep = " "

    formatted_sequence = list(map(formatter, digit_sequence))

    rows = [sep.join(formatted_sequence[i:(i+nb_digits_per_row)])
            for i in range(0, len(formatted_sequence), nb_digits_per_row)]

    sequence_block = "\n".join(rows)

    return sequence_block
