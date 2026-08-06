import math

import pytest

from operations import (
    apply_percentage,
    binary_to_decimal,
    decimal_to_binary,
    finite_average,
    imaginary_power,
    simplify_square_root,
)


def test_base_conversions():
    assert decimal_to_binary(10) == "1010"
    assert decimal_to_binary(-10) == "-1010"
    assert binary_to_decimal("-1010") == -10


def test_invalid_binary():
    with pytest.raises(ValueError):
        binary_to_decimal("102")


def test_square_root_simplification():
    assert str(simplify_square_root(72)) == "6√2"
    assert str(simplify_square_root(49)) == "7"
    assert str(simplify_square_root(0)) == "0"


def test_negative_root_rejected():
    with pytest.raises(ValueError):
        simplify_square_root(-1)


def test_average_rejects_non_finite():
    assert finite_average([1, 2, 3]) == 2
    with pytest.raises(ValueError):
        finite_average([1, math.inf])


def test_imaginary_power_supports_negative_exponents():
    assert imaginary_power(-1) == "-i"
    assert imaginary_power(4) == "1"


def test_percentage_validation():
    assert apply_percentage(100, 21) == 121
    with pytest.raises(ValueError):
        apply_percentage(-1, 21)
    with pytest.raises(ValueError):
        apply_percentage(100, -20)
