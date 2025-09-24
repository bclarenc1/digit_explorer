# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=superfluous-parens

"""
Main script for visualizing digit trajectories of mathematical constants.

This script allows you to select constants, bases, and digit counts via command-line arguments,
computes their digit sequences, converts them to trajectory points, and plots or saves the resulting images.

Usage
-----
Run from the command line with optional arguments for constants, bases, and digit counts.

Example
-------
python digit_explorer.py --constant pi --digits 31416 --base 10

@author: Benjamin Clarenc
@date:   2025-09-24
@github: bclarenc1
"""

import argparse

import matplotlib.pyplot as plt

from core.compute_digits import compute_digit_sequence, get_points_from_digits
from visu.plot_sequence import plot_sequence

MAX_DIGITS     = 100_000
DEFAULT_DIGITS = 31_416
DEFAULT_BASE   = 10

def main() -> None:
    """Parse command-line arguments and run the digit trajectory plotting workflow."""
    parser = argparse.ArgumentParser(
        description=("Plot the digit trajectory of a given constant in a given base. The image is saved in folder out/ as"
                     + " as '<constant>_<base>_<digits>.png'"),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-c", "--constant", nargs="+", type=str, default=["pi"],
                        help="constant(s) of which to plot the digit trajectory. Valid values are: 'pi', 'e', 'phi'. Default is 'pi'")
    parser.add_argument("-d", "--digits", nargs="+", type=int, default=[DEFAULT_DIGITS],
                        help=f"number(s) of digits to plot. Max is {MAX_DIGITS}. Default is {DEFAULT_DIGITS}")
    parser.add_argument("-b", "--base", nargs="+", type=int, default=[DEFAULT_BASE],
                        help=f"base(s) of the constant(s). Must be > 1. Default is {DEFAULT_BASE}")
    parser.add_argument("--show", action="store_true", default=False,
                        help="if given, show plot(s) in individual window(s). Default is False")
    parser.add_argument("--no-save", action="store_false", dest="save", default=True,
                        help="if given, do not save PNG image(s). If not, images are saved"
                        + " in folder out/ as '<constant>_<base>_<digits>.png, Default is False")
    parser.epilog = ("Examples:\n"
                + f"  python {parser.prog}                                           -> plot the first 31416 digits of pi in base 10\n"
                + f"  python {parser.prog} --constant phi --digits 20000 --base 16   -> plot the first 20000 digits of phi in base 16\n"
                + f"  python {parser.prog} -c phi -d 20000 -base 16 --show --no-save -> show the previous trajectory and do not save it\n"
                + f"  python {parser.prog} -c e pi -d 1234 5678 -b 7 11 13           -> plot the first 1234 and 5678 digits of e and pi"
                +  " in bases 7, 11 and 13, and save them in 12 separate files\n")
    args = parser.parse_args()

    # Check intputs
    # Validity of constant strings is checked later, when interpreted as numbers

    for nd in args.digits:
        if not (0 < nd <= MAX_DIGITS):
            print(f"/!\\ Invalid number of digits: {nd}, must be between 1 and {MAX_DIGITS}. Ignored")
    args.digits = [nd for nd in args.digits if 0 < nd <= MAX_DIGITS]

    for b in args.base:
        if b < 2:
            print(f"/!\\ Invalid base: {b}, must be > 1. Ignored")
    args.base = [b for b in args.base if b > 1]

    # Loopy loops
    for constant_name in args.constant:
        for base in args.base:
            for nb_digits in args.digits:
                s = "" if args.digits == 1 else "s"
                print(f"# Plotting {constant_name} in base {base} with {nb_digits:,} digit{s}")
                constant_params = (constant_name, base, nb_digits)
                digit_sequence = compute_digit_sequence(constant_name, base, nb_digits)
                pt_coords = get_points_from_digits(digit_sequence, base)
                plot_sequence(pt_coords, constant_params, bool_show=args.show, bool_save=args.save)

    if args.show:
        # keep windows open
        plt.show()


if __name__ == "__main__":
    main()
