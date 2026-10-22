from decimal import Decimal


def parse_money(a: str) -> Decimal:
    if not isinstance(a, str):
        raise TypeError

    a = a.strip()
    if a == "" or a == "-" or a == ".":
        raise ValueError

    dot = False
    minus = False
    i = 0
    prev = ""
    for ch in a:
        if minus and ch == "-":
            raise ValueError("Minus in invalid place")
        if dot:
            i += 1
            if ch == ".":
                raise ValueError("Dot is in multiple places")

        if ch == ".":
            if prev == "-":
                raise ValueError("Dot right after minus is dissaloved")
            dot = True

        if i > 2 or ch == "," or (ch != "." and ch != "-" and not ("0" <= ch <= "9")):
            raise ValueError(f"invalid money format: {a!r}")
        minus = True
        prev = ch
    q = Decimal(a).quantize(Decimal("0.01"))
    if q.is_zero():
        return abs(q)
    return q
