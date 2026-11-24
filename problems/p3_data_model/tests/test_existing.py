import pytest

from shop.cart import Cart
from shop.money import Money

pytestmark = pytest.mark.guard


def test_plus_adds_cents_in_the_same_currency():
    total = Money(120).plus(Money(350))
    assert (total.cents, total.currency) == (470, "USD")


def test_plus_rejects_a_currency_mismatch():
    with pytest.raises(ValueError):
        Money(120, "USD").plus(Money(350, "EUR"))


def test_display_formats_dollars_and_cents():
    assert Money(1205).display() == "12.05 USD"


def test_cart_subtotal_and_labels():
    cart = Cart()
    cart.put("apple", Money(120))
    cart.put("bread", Money(350))
    assert cart.subtotal().cents == 470
    assert cart.labels() == ["apple", "bread"]
