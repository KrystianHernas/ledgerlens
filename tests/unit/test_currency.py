import pytest

from ledgerlens.domain.currency import CurrencyRegistry
from ledgerlens.domain.money import Money


def test_currency_registry_contains_expected():
    reg = CurrencyRegistry()
    assert reg.decimals("PLN") == 2
    assert reg.decimals("EUR") == 2
    assert reg.decimals("USD") == 2


def test_currency_registry_unknown_raises():
    reg = CurrencyRegistry()
    with pytest.raises(ValueError, match="unknown currency"):
        reg.decimals("XYZ")


def test_money_rejects_float_amount():
    with pytest.raises(TypeError):
        Money(12.34, "PLN")


def test_money_rejects_unknown_currency():
    with pytest.raises(ValueError, match="unknown currency"):
        Money("10.00", "XYZ")


def test_money_accepts_valid():
    m = Money("10.5", "PLN")
    assert str(m.amount) == "10.50"
    assert m.currency == "PLN"