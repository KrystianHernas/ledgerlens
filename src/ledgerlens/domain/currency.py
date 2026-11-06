from typing import Final

_DEFAULT_DECIMALS: Final[dict[str, int]] = {
    "PLN": 2,
    "EUR": 2,
    "USD": 2,
}


class CurrencyRegistry:
    def __init__(self, table: dict[str, int] | None = None) -> None:
        self._table = dict(_DEFAULT_DECIMALS)
        if table:
            self._table.update({k.upper(): v for k, v in table.items()})

    def decimals(self, currency: str) -> int:
        cur = currency.upper()
        if cur not in self._table:
            raise ValueError(f"unknown currency: {currency}")
        return self._table[cur]
