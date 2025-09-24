"""
Core functions for computing digit sequences and their corresponding trajectory points.

This module provides functions to extract digit sequences of mathematical constants in
arbitrary bases, and to convert those sequences into xy-plane coordinates for visualization.
"""

from typing import Tuple, Any

from mpmath import mp
import numpy as np

from utils.digits import get_nb_digits_base_10, get_digits_in_base
from utils.plot import compute_steps, compute_points

def compute_digit_sequence(number_name: str, base: int, nb_digits: int) -> np.ndarray:
    """
    Compute the first `nb_digits` digits of a named number in a given base.

    Parameters
    ----------
    number_name : str
        Name of the mathematical constant.
    base : int
        Radix base for conversion.
    nb_digits : int
        Number of digits to extract in the given base.

    Returns
    -------
    digit_sequence : ndarray of int
        Array of digits in the given base.
    """
    if number_name == "pi":
        number = mp.pi
    elif number_name == "e":
        number = mp.e
    elif number_name == "phi":
        number = mp.phi
    else:
        print("Wait, which number?")
        raise AssertionError

    # compute 10-precision
    nb_digits_10 = get_nb_digits_base_10(base, nb_digits)
    mp.dps = nb_digits_10 + len(str(int(number)))  # need the whole part

    # compute base-b digit sequence
    digit_sequence = get_digits_in_base(number, base, nb_digits)

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
