# pylint: disable=no-member

""" TODO """

import numpy as np
import matplotlib.pyplot as plt


def compute_steps(base):
    """ TODO """
    dzs = [np.exp(1j*(np.pi/2 - 2*i*np.pi/base)) for i in range(base)]
    dxs = [dz.real for dz in dzs]
    dys = [dz.imag for dz in dzs]

    return (dxs, dys)


def compute_points(digit_sequence, dxs, dys):
    """ TODO """
    xs = np.zeros(len(digit_sequence)+1)
    ys = np.zeros(len(digit_sequence)+1)
    for i,c in enumerate(digit_sequence, start=1):
        c = int(c)
        xs[i] = xs[i-1] + dxs[c]
        ys[i] = ys[i-1] + dys[c]

    return (xs, ys)


def get_path_params(nb_digits):
    """Some number- and digits-agnostic plot params."""
    cols = [plt.cm.RdYlBu((i-1) / nb_digits) for i in range(nb_digits+1)]
    avg_step = max(1, nb_digits // 1000)

    return (cols, avg_step)


def get_latex_name(number_name):
    """Build the correct LaTeX string for the number name."""
    if number_name == "pi":
        latex_name = r"$\pi$"
    elif number_name == "e":
        latex_name = r"$e$"
    elif number_name == "phi":
        latex_name = r"$\varphi$"
    # elif number_name.startswith("sqrt"):
    #     latex_name = f"$\sqrt{number_name[4:]}$"
    else:
        # wait what?
        latex_name = number_name

    return latex_name
