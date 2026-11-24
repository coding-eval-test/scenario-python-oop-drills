# P3 — Data-model methods

**Suggested time:** 15 minutes · **Worth:** 20 points

## Context

`shop/money.py` and `shop/cart.py` work, but their objects do not behave like values.
Two `Money` objects holding the same amount are not equal, cannot be sorted, and print
as a memory address; a `Cart` cannot be measured, looped over, or searched. Every
caller works around that by reaching into the objects.

## Requirements

1. Two `Money` objects are equal when both their cents and their currency match, and
   unequal otherwise. A `Money` is never equal to something that is not a `Money`.
2. Equal `Money` objects behave as one value in a set and as the same dictionary key.
3. `Money` objects in the same currency can be compared with `<`, `<=`, `>` and `>=`,
   so `sorted(...)` and `max(...)` work on a list of them.
4. Comparing the order of two `Money` objects in different currencies raises
   `ValueError`.
5. `repr(Money(1250, "USD"))` is exactly `Money(1250, 'USD')`.
6. `len(cart)` is the number of lines in the cart.
7. Looping over a cart yields its `(label, price)` lines in the order they were added.
8. `"apple" in cart` is true when the cart has a line with that label.
9. Everything `Money` and `Cart` already do must keep working, unchanged.

## Example

```python
prices = [Money(350), Money(120), Money(120)]

print(sorted(prices))   # [Money(120, 'USD'), Money(120, 'USD'), Money(350, 'USD')]
print(len(set(prices))) # 2
```

## Running the tests

From this folder: `python -m pytest`. `tests/test_requirements.py` is what scores;
`tests/test_existing.py` covers behavior that already works and must keep working.
