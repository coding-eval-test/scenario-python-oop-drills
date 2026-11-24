"""Money as whole cents in one currency."""


class Money:
    def __init__(self, cents, currency="USD"):
        self.cents = cents
        self.currency = currency

    def plus(self, other):
        if other.currency != self.currency:
            raise ValueError("currency mismatch")
        return Money(self.cents + other.cents, self.currency)

    def display(self):
        return f"{self.cents // 100}.{self.cents % 100:02d} {self.currency}"
