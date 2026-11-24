import pytest

from shop.cart import Cart
from shop.money import Money


def make_cart():
    cart = Cart()
    cart.put("apple", Money(120))
    cart.put("bread", Money(350))
    return cart


def test_same_cents_and_currency_are_equal():
    assert Money(500) == Money(500, "USD")


def test_equality_respects_cents_currency_and_type():
    wallet = [Money(500), Money(700, "EUR")]
    assert wallet.count(Money(700, "EUR")) == 1
    assert Money(500) != Money(501)
    assert Money(500, "USD") != Money(500, "EUR")
    assert Money(500) != 500


def test_equal_money_hashes_equal():
    first, second = Money(500), Money(500)
    assert hash(first) == hash(second)


def test_money_works_in_sets_and_as_dict_keys():
    assert len({Money(500), Money(500), Money(700)}) == 2
    stock = {Money(500): "five dollars"}
    assert stock[Money(500)] == "five dollars"


def test_ordering_within_one_currency():
    assert Money(100) < Money(200)
    assert Money(200) > Money(100)
    assert Money(100) <= Money(100)
    assert Money(200) >= Money(100)
    assert not Money(200) < Money(100)


def test_sorted_and_max_work():
    prices = [Money(350), Money(120), Money(999)]
    assert [price.cents for price in sorted(prices)] == [120, 350, 999]
    assert max(prices).cents == 999


def test_ordering_across_currencies_raises_value_error():
    with pytest.raises(ValueError):
        Money(100, "USD") < Money(200, "EUR")


def test_repr_shows_how_to_rebuild_the_value():
    assert repr(Money(1250, "USD")) == "Money(1250, 'USD')"


def test_cart_has_a_length_and_iterates_in_order():
    cart = make_cart()
    assert len(cart) == 2
    assert [(label, price.cents) for label, price in cart] == [("apple", 120), ("bread", 350)]


def test_cart_membership_is_by_label():
    cart = make_cart()
    assert "apple" in cart
    assert "kiwi" not in cart
