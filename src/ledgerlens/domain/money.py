from dataclasses import dataclass
from decimal import Decimal

from ledgerlens.domain.currency import CurrencyRegistry


def _is_ascii_digit(ch: str) -> bool:
    return "0" <= ch <= "9"


def _quantize_amount(amount: Decimal, decimals: int) -> Decimal:
    if decimals <= 0:
        quant = Decimal(1)
    else:
        quant = Decimal("0." + "0" * (decimals - 1) + "1")
    q = amount.quantize(quant, rounding="ROUND_HALF_UP")
    if q.is_zero():
        return abs(q)
    return q


def parse_money(a: str) -> Decimal:
    if not isinstance(a, str):
        raise TypeError("Input is not a string")

    a = a.strip()
    if len(a) > 20:
        raise ValueError(f"input too long: {len(a)} characters")
    s = a.split(".")

    if len(s) > 2:
        raise ValueError("Dot is in multiple places")

    seen_char = False
    for ch in a:
        if seen_char and ch == "-":
            raise ValueError("Minus in invalid place")

        if ch != "." and ch != "-" and not _is_ascii_digit(ch):
            raise ValueError(f"invalid money format: {a!r}")

        seen_char = True

    if not any(_is_ascii_digit(ch) for ch in a):
        raise ValueError("Input does not contain digit")

    integer_part = s[0].lstrip("-")

    if len(integer_part) > 16:
        raise ValueError("Number is too big")

    return Decimal(a)


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __init__(
        self,
        amount: Decimal | str,
        currency: str,
        registry: CurrencyRegistry | None = None,
    ) -> None:
        reg = registry or CurrencyRegistry()
        cur = currency.upper()
        dec = reg.decimals(cur)
        if isinstance(amount, str):
            amt = parse_money(amount)
            amt = _quantize_amount(amt, dec)
        elif isinstance(amount, Decimal):
            amt = _quantize_amount(amount, dec)
        else:
            raise TypeError("amount must be Decimal or str")
        object.__setattr__(self, "amount", amt)
        object.__setattr__(self, "currency", cur)
