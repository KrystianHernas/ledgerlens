test przechodził z innego powodu (parse_money i "1e3" przy zbyt ogólnym ValueError),
InvalidOperation wyciekał z quantize przy 30 cyfrach, bo kontekst Decimal ma precyzję 28,
reguła „musi być cyfra” działała tylko przypadkiem, dopóki nie usunęliśmy warunku z prev == "-",
test granicy 64 znaków był zaprojektowany tak, że wcześniejsza walidacja łapała wejście pierwsza.

24.10.2026
zera wiodące odpowiedź brzmiała logicznie ale nie zgadzała sie z kodem
test z match="too many zeros" przechodził przez guard długości, zanim doszedł do limitu cyfr,
InvalidOperation z quantize przy 30 cyfrach, bo precyzja kontekstu Decimal to 28.

27.10.2026 (M2)
CurrencyRegistry.normalizes do uppercase, a nie odrzuca małe litery — decyzja niezawarta w teście.
parse_money twardo zakłada 2 miejsca (quantize 0.01), Money nie używa CurrencyRegistry.decimals przy kwantyzacji.
Money.__init__ tworzy nowy CurrencyRegistry przy każdym wywołaniu — brak wstrzykiwania zależności.
float odrzucany przez TypeError, ale komunikat nie wskazuje dozwolonych typów (Decimal | str).

