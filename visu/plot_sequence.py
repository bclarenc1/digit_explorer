""" TODO """

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from utils.plot import get_latex_name, get_path_params

def add_inset(ax, base, legend_position="upper right"):
    """ TODO """
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


def plot_sequence(pt_coords, number_params, legend_position="upper right", bool_save=True):
    """Plot the colored path of the digit sequence."""
    xs, ys = pt_coords
    number_name, base, nb_digits = number_params
    cols, avg_step = get_path_params(nb_digits)

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
    latex_name = get_latex_name(number_name)
    ax.set_title(f"{nb_digits:,} digits of {latex_name} (base {base})")

    # save figure?
    if bool_save:
        savepath = f"out/{number_name}_{base:02d}_{nb_digits:06d}.png"
        fig.savefig(savepath)
        print(f"Plot saved: {savepath}")
