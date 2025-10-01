# pylint: disable=no-member

"""
Utility functions for plotting digit trajectories.

This module provides functions to compute step directions, generate trajectory points,
set plotting parameters, and build LaTeX names for numbers.
"""

from typing import List, Tuple, Any

import numpy as np
import matplotlib.pyplot as plt

def compute_steps(base: int) -> Tuple[List[float], List[float]]:
    """
    Compute the directions of unit displacements in the given base.

    Parameters
    ----------
    base : int
        Radix base (number of possible directions).

    Returns
    -------
    dxs : list of float
        List of x-components for each direction.
    dys : list of float
        List of y-components for each direction.
    """
    dzs = [np.exp(1j*(np.pi/2 - 2*i*np.pi/base)) for i in range(base)]
    dxs = [dz.real for dz in dzs]
    dys = [dz.imag for dz in dzs]

    return (dxs, dys)


def compute_points(digit_sequence: Any, dxs: List[float], dys: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the trajectory points from a digit sequence and step directions.

    Parameters
    ----------
    digit_sequence : array-like of int
        Sequence of digits representing the path.
    dxs : list of float
        List of x-components for each direction.
    dys : list of float
        List of y-components for each direction.

    Returns
    -------
    xs : ndarray of float
        Array of x-coordinates of the trajectory.
    ys : ndarray of float
        Array of y-coordinates of the trajectory.
    """
    xs = np.zeros(len(digit_sequence)+1)
    ys = np.zeros(len(digit_sequence)+1)
    for i, c in enumerate(digit_sequence, start=1):
        c = int(c)
        xs[i] = xs[i-1] + dxs[c]
        ys[i] = ys[i-1] + dys[c]

    return (xs, ys)


def generate_path_params(nb_digits: int) -> Tuple[List[Any], int]:
    """
    Generate plotting parameters for a digit trajectory.

    Parameters
    ----------
    nb_digits : int
        Number of digits in the sequence.

    Returns
    -------
    cols : list
        List of colors for trajectory points.
    avg_step : int
        Distance between 2 plotted points.
    """
    cols = [plt.cm.RdYlBu((i-1) / nb_digits) for i in range(nb_digits+1)]
    avg_step = max(1, nb_digits // 1000)

    return (cols, avg_step)


def build_latex_name(number_name: str) -> str:
    """
    Build the LaTeX string for the name of the given number.

    Parameters
    ----------
    number_name : str
        Name of the number (e.g., "pi", "e", "sqrt2").

    Returns
    -------
    latex_name : str
        LaTeX-formatted string for the number.
    """
    if number_name == "pi":
        latex_name = r"$\pi$"
    elif number_name == "e":
        latex_name = r"$e$"
    elif number_name == "phi":
        latex_name = r"$\varphi$"
    elif number_name.startswith("sqrt"):
        latex_name = fr"$\sqrt{{{number_name[4:]}}}$"
    else:
        latex_name = number_name

    return latex_name
