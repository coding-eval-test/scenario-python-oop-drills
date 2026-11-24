# P1 — Custom exception hierarchy

**Suggested time:** 15 minutes · **Worth:** 20 points

## Context

`payments/processor.py` charges accounts through a payment gateway. When a charge
cannot go through, it raises a bare `Exception` or `ValueError` with a short string, so
callers cannot tell one failure from another or read any detail off the error.
`payments/errors.py` holds placeholder classes for the errors the team wants instead.

## Requirements

1. `PaymentError` is an exception, and it is the common base of the other four errors in
   `payments/errors.py` — catching it catches any of them.
2. Charging an account that was never registered raises `AccountNotFoundError`. The
   error exposes `account_id`, and its message reads `Account 'A-9' not found`.
3. Charging zero or a negative amount raises `InvalidAmountError`. The error exposes
   `amount`, and its message reads `Amount must be positive, got -5`.
4. Charging more than the balance raises `InsufficientFundsError`. The error exposes
   `account_id`, `balance`, `requested`, and `shortfall` (how much is missing), and its
   message reads `Account 'A-1' has 50 but 80 was requested`.
5. Code already in production catches `ValueError` for the failures in requirements 3
   and 4. It must keep working, unchanged.
6. When the gateway raises `ConnectionError`, the charge raises `GatewayError`, which
   exposes `account_id`. The original `ConnectionError` stays attached as the cause of
   the new error, and the account's balance does not change.

How each error is constructed is up to you — the tests only ever trigger them through
`PaymentProcessor.charge`.

## Example

```python
processor = PaymentProcessor(gateway)
processor.register(Account("A-1", 50))

try:
    processor.charge("A-1", 80)
except PaymentError as error:
    print(error)            # Account 'A-1' has 50 but 80 was requested
    print(error.shortfall)  # 30
```

## Running the tests

From this folder: `python -m pytest`. `tests/test_requirements.py` is what scores;
`tests/test_existing.py` covers behavior that already works and must keep working.
