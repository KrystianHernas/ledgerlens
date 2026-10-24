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
    assert str(parse_money(" 12.5 ")) == "12.50"


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


def test_multiple_dots():
    with pytest.raises(ValueError):
        parse_money("1.2.3")


def test_only_minus():
    with pytest.raises(ValueError):
        parse_money("-")


def test_whitespace_inside():
    with pytest.raises(ValueError):
        parse_money("1 000")


def test_arabic_numbers():
    with pytest.raises(ValueError):
        parse_money("\u0661\u0662.\u0665")


def test_minus_inside():
    with pytest.raises(ValueError):
        parse_money("1-2")


def test_double_minus():
    with pytest.raises(ValueError):
        parse_money("--1")


def test_dot():
    with pytest.raises(ValueError):
        parse_money(".")


def test_minus_dot():
    with pytest.raises(ValueError):
        parse_money("-.")


def test_dot_minus():
    with pytest.raises(ValueError):
        parse_money("1.-2")


def test_negative_zero():
    assert str(parse_money("-0.00")) == "0.00"


def test_negative_zero_integer():
    assert str(parse_money("-0")) == "0.00"


def test_leading_dot():
    assert str(parse_money(".5")) == "0.50"


def test_leading_dot_with_minus():
    assert str(parse_money("-.5")) == "-0.50"


def test_trailing_dot():
    assert str(parse_money("5.")) == "5.00"


def test_16_integer_digits_accepted():
    assert str(parse_money("1" * 16)) == "1" * 16 + ".00"


def test_17_integer_digits_rejected():
    with pytest.raises(ValueError):
        parse_money("1" * 17)


def test_16_integer_digits_with_minus_accepted():
    assert str(parse_money("-" + "1" * 16)) == "-" + "1" * 16 + ".00"


def test_16_integer_digits_with_fraction_accepted():
    assert str(parse_money("1" * 16 + ".5")) == "1" * 16 + ".50"


def test_max_length_accepted():
    assert str(parse_money("-" + "1" * 16 + ".99")) == "-1111111111111111.99"


def test_surrounding_whitespace_not_counted():
    assert str(parse_money(" " * 60 + "12.5")) == "12.50"


def test_length_over_limit_rejected():
    with pytest.raises(ValueError, match="too long"):
        parse_money("0" * 21)


def test_20_chars_of_zeros_rejected_by_digit_limit():
    with pytest.raises(ValueError):
        parse_money("0" * 20)


def test_too_many_leading_zeros():
    with pytest.raises(ValueError, match="Number is too big"):
        parse_money("0" * 16 + "1")


def test_20_chars_with_19_digits_rejected():
    with pytest.raises(ValueError):
        parse_money("-" + "1" * 19)
