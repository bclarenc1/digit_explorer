# pylint: disable=eval-used
# pylint: disable=broad-exception-caught

""" TODO """

from typing import Any
import warnings

from mpmath import mp, mpc

def is_constant(attr_str: str) -> bool:
    """For a given attribute string, return True iff the attribute is a constant (pi, e, etc.)
    """
    try:
        attr = getattr(mp, attr_str)
        return hasattr(attr, '__class__') and attr.__class__.__name__ == 'constant'
    except Exception:
        return False


def build_env() -> dict:
    """
    Construit l'environnement autorisé avec toutes les
    fonctions et constantes publiques de mpmath.
    """
    standard_fcts = ["sqrt", "exp", "ln", "log", "log10",
                    "cos", "sin", "tan", "cosh", "sinh", "tanh", "asin", "acos", "atan"]
    standard_csts = [attr_str for attr_str in dir(mp) if is_constant(attr_str)]
    standard_attrs = standard_fcts + standard_csts
    env = {attr: getattr(mp, attr) for attr in standard_attrs}

    # env["log2"] = "lambda x: mp.log(x, 2)"

    return env


def parse_expr(expr: str) -> Any:
    """
    Évalue une expression utilisateur avec mpmath
    dans un environnement limité.
    """
    mp_env = build_env()
    try:
        x = eval(expr, {"__builtins__": None}, mp_env)
        if isinstance(x, mpc):
            warnings.warn("Complex expression. Imaginary part was discarded")
            x = x.real
        return x
    except Exception as e:
        raise ValueError(f"Invald expression: {expr}\n{e}") from e
