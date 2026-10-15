from decimal import Decimal

import pytest

from ledgerlens.domain.money import parse_money


def test_zero():
    assert str(parse_money("0.00")) == str(Decimal("0.00"))


def test_negative():
    assert str(parse_money("-0.01")) == str(Decimal("-0.01"))


def test_one_precision():
    assert str(parse_money("12.5")) == str(Decimal("12.50"))


def test_whitespace():
    assert str(parse_money(" 12.5 ")) == str(Decimal("12.50"))


def test_three_precision():
    with pytest.raises(ValueError):
        parse_money("0.001")


def test_e_precision():
    with pytest.raises(ValueError):
        parse_money("1e3")


def test_thousand_separator():
    with pytest.raises(ValueError):
        parse_money("1,000.00")


def test_empty():
    with pytest.raises(ValueError):
        parse_money("")


def test_string():
    with pytest.raises(ValueError):
        parse_money("abc")
