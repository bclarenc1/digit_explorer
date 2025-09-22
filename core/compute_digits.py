""" TODO """

from mpmath import mp

from utils.digits import get_nb_digits_base_10, get_digits_in_base
from utils.plot import compute_steps, compute_points

def compute_digit_sequence(number_name, base, nb_digits):
    """Compute the first 'nb_digits' digits of a named number in base 'base'."""
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


def get_points_from_digits(digit_sequence, base):
    """Convert a sequence of digits into a sequence of points on the xy plane."""
    dxs, dys = compute_steps(base)
    xs, ys   = compute_points(digit_sequence, dxs, dys)

    return (xs, ys)
