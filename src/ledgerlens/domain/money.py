from dataclasses import dataclass
from decimal import Decimal

from ledgerlens.domain.currency import CurrencyRegistry


def _is_ascii_digit(ch: str) -> bool:
    return "0" <= ch <= "9"


def parse_money(a: str) -> Decimal:
    if not isinstance(a, str):
        raise TypeError("Input is not a string")

    a = a.strip()
    if len(a) > 20:
        raise ValueError(f"input too long: {len(a)} characters")
    s = a.split(".")

    if len(s) > 2:
        raise ValueError("Dot is in multiple places")
    if len(s) == 2 and len(s[1]) > 2:
        raise ValueError("More than 2 decimal places")

    seen_char = False
    for ch in a:
        if seen_char and ch == "-":
            raise ValueError("Minus in invalid place")

        # allowed characters only
        if ch != "." and ch != "-" and not _is_ascii_digit(ch):
            raise ValueError(f"invalid money format: {a!r}")

        seen_char = True

    if not any(_is_ascii_digit(ch) for ch in a):
        raise ValueError("Input does not contain digit")

    # Leading zeros count toward the 16-digit limit (decision B).
    integer_part = s[0].lstrip("-")

    if len(integer_part) > 16:
        raise ValueError("Number is too big")

    q = Decimal(a).quantize(Decimal("0.01"))
    if q.is_zero():
        return abs(q)
    return q


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __init__(self, amount: Decimal | str, currency: str) -> None:
        registry = CurrencyRegistry()
        cur = currency.upper()
        registry.decimals(cur)  # validates
        if isinstance(amount, str):
            amt = parse_money(amount)
        elif isinstance(amount, Decimal):
            amt = amount
        else:
            raise TypeError("amount must be Decimal or str")
        object.__setattr__(self, "amount", amt)
        object.__setattr__(self, "currency", cur)
