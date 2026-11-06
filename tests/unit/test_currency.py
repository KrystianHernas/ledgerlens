from decimal import Decimal

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


def test_money_accepts_lowercase_currency_normalized():
    m = Money("10.00", "pln")
    assert m.currency == "PLN"
    m2 = Money("10.00", "Eur")
    assert m2.currency == "EUR"


def test_money_accepts_decimal_amount():
    m = Money(Decimal("10.5"), "PLN")
    assert str(m.amount) == "10.50"
    assert m.currency == "PLN"


def test_money_quantizes_per_currency_registry():
    reg = CurrencyRegistry({"JPY": 0, "BHD": 3})
    m_jpy = Money("10.5", "JPY", registry=reg)
    assert str(m_jpy.amount) == "11"
    assert m_jpy.currency == "JPY"

    m_bhd = Money("10.1234", "BHD", registry=reg)
    assert str(m_bhd.amount) == "10.123"
    assert m_bhd.currency == "BHD"

    m_pln = Money("10.5", "PLN", registry=reg)
    assert str(m_pln.amount) == "10.50"
    assert m_pln.currency == "PLN"


def test_money_uses_default_registry_when_none_provided():
    m = Money("10.5", "PLN")
    assert str(m.amount) == "10.50"
    assert m.currency == "PLN"