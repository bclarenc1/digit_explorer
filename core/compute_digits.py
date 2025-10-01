"""
Core functions for computing digit sequences and their corresponding trajectory points.

This module provides functions to extract digit sequences of mathematical constants in
arbitrary bases, and to convert those sequences into xy-plane coordinates for visualization.
"""

from typing import Tuple, Any

import numpy as np
from mpmath import mp, floor, log10, fabs

from utils.digits import get_nb_digits_base_10, get_digits_in_base, format_digit_sequence
from utils.plot import compute_steps, compute_points
from utils.expression import parse_expr, build_basename

def compute_digit_sequence(expr: str, base: int, nb_digits: int,
                           bool_disp: bool = False, bool_save: bool = True
                           ) -> np.ndarray:  # type: ignore
    """
    Compute the first ``nb_digits`` digits of a constant in a given base.

    Parameters
    ----------
    expr : str
        String expression representing a number.
    base : int
        Radix base for conversion.
    nb_digits : int
        Number of digits to extract in the given base.
    bool_save : bool
        If ``True``, save the digit sequence in a text file

    Returns
    -------
    digit_sequence : ndarray of int
        Array of digits in the given base.
    """

    # convert expression into rough mpf number.
    # on the first iteration, eval() uses the default precision (15 significant digits);
    # so we will need to re-eval() later with the precision needed.
    # Fortunately we just need the whole part here
    number_rough = parse_expr(expr)

    # compute precision in base 10.
    # mp.dps is the number of significant digits, including the whole part,
    # and excluding leading 0s in small numbers (like 0.004):
    # it must be adjusted for all cases
    # if   1 <= |x|,       shift = number of digits in int(|x|)
    # if 0.1 <= |x| < 1,   shift = 0
    # if        |x| < 0.1, shift = -1*(number of leading 0s in the decimal places)
    nb_digits_10 = get_nb_digits_base_10(base, nb_digits)
    shift = floor(log10(fabs(number_rough))) + 1
    mp.dps = nb_digits_10 + shift
    number = parse_expr(expr)

    # compute base-b digit sequence
    digit_sequence = get_digits_in_base(number, base, nb_digits)

    # show or display sequence?
    if bool_save or bool_disp:
        sequence_block = format_digit_sequence(digit_sequence, base)
        if bool_disp:
            print(f"First {nb_digits} digits of '{expr}' in base {base} (rounded):")
            print(sequence_block)
        if bool_save:
            basename = build_basename(expr)
            savepath = f"out/{basename}_{base:03d}_{nb_digits:06d}.txt"
            with open(savepath, mode="w", encoding="utf-8") as f:
                f.write(sequence_block)
            print(f"  Sequence saved: {savepath}")

    return digit_sequence


def get_points_from_digits(digit_sequence: Any, base: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert a sequence of digits into a sequence of points on the xy plane.

    Parameters
    ----------
    digit_sequence : array-like of int
        Sequence of digits representing the path.
    base : int
        Radix base (number of possible directions).

    Returns
    -------
    xs : ndarray of float
        Array of x-coordinates of the trajectory.
    ys : ndarray of float
        Array of y-coordinates of the trajectory.
    """
    dxs, dys = compute_steps(base)
    xs, ys   = compute_points(digit_sequence, dxs, dys)

    return (xs, ys)
