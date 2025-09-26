# pylint: disable=eval-used
# pylint: disable=broad-exception-caught

"""
Utility functions and constants for building the restricted mathematical environment of mpmath.

This module exposes standard functions and constants from mpmath, in order to allow the evaluation
of safe expressions only.

Constants
---------
STANDARD_FCTS : list of str
    Names of the standard mathematical functions (e.g., "sqrt", "log", "sin").
STANDARD_CSTS : list of str
    Names of the standard mathematical constants provided by ``mpmath`` (e.g., "pi", "e").
STANDARD_ATTRS : list of str
    Combined list of these standard functions and constants exposed in the environment.
"""

from typing import Any
import warnings

from mpmath import mp, mpc

def is_constant(attr_str: str) -> bool:
    """
    Check whether a given attribute name corresponds to a mathematical constant.

    Parameters
    ----------
    attr_str : str
        Name of an attribute from the ``mpmath`` module.

    Returns
    -------
    bool
        ``True`` if the attribute is a constant (e.g., "pi", "e"), ``False`` otherwise.
    """
    try:
        attr = getattr(mp, attr_str)
        return hasattr(attr, '__class__') and attr.__class__.__name__ == 'constant'
    except Exception:
        return False


STANDARD_FCTS = ["sqrt", "exp",  "ln",   "log",   "log10",
                 "sin",  "cos",  "tan",  "sinh",  "cosh",  "tanh",
                 "asin", "acos", "atan", "asinh", "acosh", "atanh"]

STANDARD_CSTS = [attr_str for attr_str in dir(mp) if (is_constant(attr_str) and attr_str != "eps")]
# epsilon causes issues and is not a math constant anyway

STANDARD_ATTRS = STANDARD_FCTS + STANDARD_CSTS


def build_env() -> dict:
    """
    Construct the restricted mathematical environment.

    This environment is a dictionary mapping attribute names to the corresponding
    attribute (functions or constants) from ``mpmath``.

    Returns
    -------
    dict
        Dictionary of allowed names with their corresponding ``mpmath`` attribute.
    """
    env = {attr: getattr(mp, attr) for attr in STANDARD_ATTRS}

    return env


def parse_expr(expr: str) -> Any:
    """
    Evaluate a mathematical expression within the restricted environment.

    The expression is evaluated with ``eval`` using only the functions and
    constants from ``mpmath`` defined in the restricted environment.
    If the result is a complex number, the imaginary part is discarded and
    a warning is issued.

    Parameters
    ----------
    expr : str
        User-provided mathematical expression (e.g., ``"sin(log(sqrt(5*pi/e)))"``).

    Returns
    -------
    Any
        Result of the evaluated expression. If complex, the real part is returned.

    Raises
    ------
    ValueError
        If the expression is invalid or the evaluation fails.
    """
    mp_env = build_env()
    try:
        x = eval(expr, {"__builtins__": None}, mp_env)
        if isinstance(x, mpc):
            warnings.warn("Complex result. Imaginary part was discarded")
            x = x.real
        return x
    except Exception as e:
        raise ValueError(f"Invald expression: {expr}\n{e}") from e
