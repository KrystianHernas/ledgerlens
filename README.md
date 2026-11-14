# LedgerLens

LedgerLens is a backend library for handling monetary amounts and currencies,
and a foundation for a future financial application. The project is mainly
a hands-on way to practice backend engineering: test-driven development,
strict typing, precise `Decimal` handling, and reasoning through business decisions.

> **Status:** early development (Milestone 2): money parsing and currency handling.

## Features (so far)

- `parse_money(str) -> Decimal`: strict money-string parsing
  (ASCII digits, optional leading minus, single dot; rejects floats, exponents,
  thousand separators, non-Latin digits).
- `CurrencyRegistry`: currency → number of decimal places
  (defaults: PLN, EUR, USD = 2; custom tables supported, e.g. JPY = 0, BHD = 3).
- `Money`: immutable value object (`amount: Decimal`, `currency: str`),
  quantized to the currency's decimal places with `ROUND_HALF_UP`.

```python
from ledgerlens.domain.currency import CurrencyRegistry
from ledgerlens.domain.money import Money

Money("10.5", "pln")                # Money(amount=Decimal('10.50'), currency='PLN')

reg = CurrencyRegistry({"JPY": 0})
Money("10.5", "JPY", registry=reg)  # Money(amount=Decimal('11'), currency='JPY')
```

## Requirements

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
git clone git@github.com:KrystianHernas/ledgerlens.git
cd ledgerlens
uv sync
```

## Development

```bash
uv run pytest          # tests
uv run ruff check .    # lint
uv run mypy src        # type check (strict)
```

Workflow: test first, then implementation (one `test:` commit, then one `feat:` commit per milestone).

## Project layout

```
src/ledgerlens/domain/   # domain model: money, currency
tests/unit/              # unit tests
docs/learning-log.md     # lessons learned per milestone
```
