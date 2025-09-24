# pylint: disable=too-many-locals

"""Methods for plotting a digit trajectory."""

from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.axes import Axes

from utils.plot import generate_path_params, build_latex_name

def add_inset(ax: Axes, base: int, legend_position: str = "upper right") -> None:
    """
    Add a custom inset legend to the given axis, showing direction for each digit.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to which the inset will be added.
    base : int
        Radix base (number of possible directions).
    legend_position : str, optional
        Position of inset legend (default is "upper right").
    """

    inset_ax = inset_axes(ax, width="20%", height="20%", loc=legend_position)
    inset_ax.set_aspect('equal')
    inset_ax.axis('off')
    nb_spokes = base
    angles = np.pi/2 - np.linspace(0, 2*np.pi, nb_spokes, endpoint=False)
    x_spokes, y_spokes = np.cos(angles), np.sin(angles)
    x_labels, y_labels = np.cos(angles-1./nb_spokes), np.sin(angles-1./nb_spokes)
    for i in range(nb_spokes):
        inset_ax.plot([0, x_spokes[i]], [0, y_spokes[i]], color='white', lw=1)
        inset_ax.annotate("", xy=(x_spokes[i], y_spokes[i]), xytext=(0,0),
                          arrowprops={"arrowstyle":"->", "lw":1, "mutation_scale":15})
        inset_ax.text(x_labels[i], y_labels[i], str(i), ha='center', va='center', fontsize=10)


def plot_sequence(pt_coords: Tuple[np.ndarray, np.ndarray],
                  number_params: Tuple[str, int, int], legend_position: str = "upper right",
                  bool_show: bool = False, bool_save: bool = True) -> None:
    """
    Plot the colored path of the digit sequence.

    Parameters
    ----------
    pt_coords : tuple of ndarray
        (xs, ys) coordinates of the digit sequence.
    number_params : tuple
        (number_name, base, nb_digits) for the sequence.
    legend_position : str, optional
        Position of inset legend (default is "upper right").
    bool_show : bool, optional
        If True, display the plot (default is False).
    bool_save : bool, optional
        If True, save the plot (default is True).
    """
    xs, ys = pt_coords
    number_name, base, nb_digits = number_params
    cols, avg_step = generate_path_params(nb_digits)

    fig, ax = plt.subplots(1, 1, figsize=(8,8))

    # path
    ax.scatter(xs, ys, color=cols, marker="o", s=1)
    ax.plot(xs[::avg_step], ys[::avg_step], color="gray", linestyle="-", linewidth=1, alpha=.9)

    # axes, start, stop and inset
    mk, ms, mfc = "o", 15, "none"
    ax.axhline(y=0, c="k", ls="--", lw=1)
    ax.axvline(x=0, c="k", ls="--", lw=1)
    ax.plot(xs[0],  ys[0],  color=cols[0],  marker=mk, ms=ms, markerfacecolor=mfc)
    ax.plot(xs[-1], ys[-1], color=cols[-1], marker=mk, ms=ms, markerfacecolor=mfc)
    add_inset(ax, base, legend_position)

    # title
    latex_name = build_latex_name(number_name)
    ax.set_title(f"{nb_digits:,} digits of {latex_name} (base {base})")

    # show or save figure?
    if bool_save:
        savepath = f"out/{number_name}_{base:02d}_{nb_digits:06d}.png"
        fig.savefig(savepath)
        print(f"  Plot saved: {savepath}")
    if bool_show:
        fig.show()
    else:
        plt.close(fig)
