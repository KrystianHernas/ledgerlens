from decimal import Decimal


def parse_money(a: str) -> Decimal:
    if not isinstance(a, str):
        raise TypeError("Input is not a string")

    a = a.strip()
    if len(a) > 64:
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

        # reguła dozwolonych znaków
        if ch != "." and ch != "-" and not ("0" <= ch <= "9"):
            raise ValueError(f"invalid money format: {a!r}")

        seen_char = True

    if not any("0" <= ch <= "9" for ch in a):
        raise ValueError("Input does not contain digit")

    integer_part = s[0].lstrip("-")

    if len(integer_part) > 16:
        raise ValueError("Number is too big")

    q = Decimal(a).quantize(Decimal("0.01"))
    if q.is_zero():
        return abs(q)
    return q
