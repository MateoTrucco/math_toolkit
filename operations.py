"""Pure operations for the desktop math toolkit."""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import fmean


def decimal_to_binary(value: int) -> str:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    sign = "-" if value < 0 else ""
    return sign + format(abs(value), "b")


def binary_to_decimal(value: str) -> int:
    normalized = value.strip().replace("_", "")
    if normalized.startswith(("+", "-")):
        sign, digits = normalized[0], normalized[1:]
    else:
        sign, digits = "", normalized
    if not digits or any(character not in "01" for character in digits):
        raise ValueError("binary input may contain only 0 and 1")
    number = int(digits, 2)
    return -number if sign == "-" else number


@dataclass(frozen=True)
class SimplifiedRoot:
    coefficient: int
    radicand: int

    def __str__(self) -> str:
        if self.radicand == 1:
            return str(self.coefficient)
        if self.coefficient == 1:
            return f"√{self.radicand}"
        return f"{self.coefficient}√{self.radicand}"


def simplify_square_root(value: int) -> SimplifiedRoot:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    if value < 0:
        raise ValueError("real square roots require a non-negative integer")
    if value == 0:
        return SimplifiedRoot(0, 1)

    coefficient = 1
    radicand = value
    factor = 2
    while factor * factor <= radicand:
        square = factor * factor
        while radicand % square == 0:
            coefficient *= factor
            radicand //= square
        factor += 1
    return SimplifiedRoot(coefficient, radicand)


def finite_average(values: list[float]) -> float:
    if not values:
        raise ValueError("at least one number is required")
    if any(not math.isfinite(value) for value in values):
        raise ValueError("all numbers must be finite")
    return fmean(values)


def imaginary_power(exponent: int) -> str:
    if not isinstance(exponent, int) or isinstance(exponent, bool):
        raise TypeError("exponent must be an integer")
    return ("1", "i", "-1", "-i")[exponent % 4]


def apply_percentage(base: float, percentage: float) -> float:
    if not math.isfinite(base) or not math.isfinite(percentage):
        raise ValueError("values must be finite")
    if base < 0:
        raise ValueError("base amount cannot be negative")
    if percentage < 0 or percentage > 1000:
        raise ValueError("percentage must be between 0 and 1000")
    return base * (1 + percentage / 100)
