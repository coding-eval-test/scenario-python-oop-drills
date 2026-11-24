"""A shopping cart: named lines, each with a price."""
from shop.money import Money


class Cart:
    def __init__(self):
        self._lines = []

    def put(self, label, price):
        self._lines.append((label, price))

    def subtotal(self):
        running = Money(0)
        for _, price in self._lines:
            running = running.plus(price)
        return running

    def labels(self):
        return [label for label, _ in self._lines]
