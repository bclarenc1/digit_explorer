# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=superfluous-parens

"""
Main script for visualizing digit trajectories of mathematical constants and expressions.

This script allows you to select expressions, bases, and number of digits via command-line arguments,
computes the digit sequences, converts them to trajectory points, and plots or saves the resulting images and sequences.

Usage
-----
Run from the command line with optional arguments for expressions, bases, and number of digits.

Examples
--------
python digit_explorer.py --expr "pi" --digits "31416" --base "10"
python digit_explorer.py --expr "phi-1" "sin(log10(sqrt(pi/e**2))" --digits "69" "420" "69420" --base "8" "16" "123"


@author: Benjamin Clarenc
@date:   2025-10-01
@github: bclarenc1
"""

import argparse

import matplotlib.pyplot as plt

from core.compute_digits import compute_digit_sequence, get_points_from_digits
from visu.plot_sequence import plot_sequence
from utils.expression import STANDARD_FCTS, STANDARD_CSTS

MAX_DIGITS     = 100_000
DEFAULT_DIGITS = 31_416
DEFAULT_BASE   = 10


def main() -> None:
    """Parse command-line arguments and run the digit trajectory plotting workflow."""

    parser = argparse.ArgumentParser(
        description=("Plot the digit trajectory of a given constant or expression in a given base. The image and the digit sequence"
                     + " are saved in folder out/ as '<expression>_<base>_<digits>.png' and '(idem).txt'"),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-e", "--expr", "--expression", nargs="+", type=str, default=["pi"], dest="expr",
                        help="expressions(s) of which to plot the digit trajectory. Expressions can be constants (see examples). Default is 'pi'")
    parser.add_argument("-d", "--digits", nargs="+", type=int, default=[DEFAULT_DIGITS],
                        help=f"number(s) of digits to plot. Max is {MAX_DIGITS}. Default is {DEFAULT_DIGITS}")
    parser.add_argument("-b", "--base", nargs="+", type=int, default=[DEFAULT_BASE],
                        help=f"base(s) of the expression(s). Must be > 1. Default is {DEFAULT_BASE}")
    parser.add_argument("--show", action="store_true", default=False,
                        help="if given, show plot(s) in individual window(s). Default is False")
    parser.add_argument("--disp", action="store_true", default=False,
                        help="if given, display the digit sequence. Default is False")
    parser.add_argument("--no-save", action="store_false", dest="save", default=True,
                        help="if given, do not save PNG image(s) nor text file(s). If not, images and sequences"
                        + " are saved in folder out/ as '<expr>_<base>_<digits>.png' and '(idem).txt', Default is False")
    parser.add_argument("-l", "--list", action="store_true",
                        help="if given, show the lists of valid mathematical functions and constants.")

    parser.epilog = ("Examples:\n"
                  + f'  python {parser.prog}                                                 -> plot the first 31416 digits of pi in base 10\n'
                  + f'  python {parser.prog} --expr "phi" --digits 2000 --base 16 --disp     -> plot the first 2000 digits of phi in base 16 and display them in plain text\n'
                  + f'  python {parser.prog} -e "phi" -d 20000 -base 16 --show --no-save     -> show the previous trajectory and do not save it, nor the digits\n'
                  + f'  python {parser.prog} -e "e" "pi" -d 1234 5678 -b 7 11 13             -> plot the first 1234 and 5678 digits of e and pi'
                  +  ' in bases 7, 11 and 13, and save them in 12 separate PNG files and 12 separate text files\n'
                  + f'  python {parser.prog} -e "sin(log10(sqrt(apery**3/(euler+1))))" -d 50 -> plot the first 50 digits of this awful expression\n\n'
                  +  'Important note:\n'
                  +  '  An expression cannot start with "-" (like --expr "-2*pi"). Either add an initial space (--expr " -2*pi")'
                  +  ' or rephrase the expression (--expr "pi*(-2)").\n\n'
                  +  'Note for --nerds-- astute users:\n'
                  +  '  You may have noticed that the very last digits are sometimes rounded up. This is due to how digits are computed given a precision.\n')
    args = parser.parse_args()

    # Check inputs
    if args.list:
        print("Valid functions:\n  " + ", ".join(STANDARD_FCTS))
        print("Valid constants:\n  " + ", ".join(STANDARD_CSTS))
        return

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
    for expr in args.expr:
        for base in args.base:
            for nb_digits in args.digits:
                s = "" if args.digits == 1 else "s"
                print(f"# Plotting {expr} in base {base} with {nb_digits:,} digit{s}")
                constant_params = (expr, base, nb_digits)
                digit_sequence = compute_digit_sequence(expr, base, nb_digits,
                                                        bool_disp=args.disp, bool_save=args.save)
                pt_coords = get_points_from_digits(digit_sequence, base)
                plot_sequence(pt_coords, constant_params, bool_show=args.show, bool_save=args.save)

    if args.show:
        # keep windows open
        plt.show()


if __name__ == "__main__":
    main()
