# pylint: disable=invalid-name

""" TODO """

from core.compute_digits import compute_digit_sequence, get_points_from_digits
from visu.plot_sequence import plot_sequence

number_name = "pi"
base = 10
nb_digits = 10001
number_params = number_name, base, nb_digits

if __name__ == "__main__":
    digit_sequence = compute_digit_sequence(number_name, base, nb_digits)
    pt_coords = get_points_from_digits(digit_sequence, base)
    plot_sequence(pt_coords, number_params, bool_save=True)
