# P5 — Properties and validation

**Suggested time:** 15 minutes · **Worth:** 20 points

## Context

`bank/account.py` keeps everything in plain public fields. Nothing stops code from
setting a balance to a negative number or a string, overdrawing an account, or
renaming an account's id after it was opened. `InvalidBalanceError` is a placeholder
for the error the team wants raised instead.

## Requirements

1. `InvalidBalanceError` is a `ValueError`.
2. `balance` is a property, so a balance is checked every time it is assigned — by
   outside code, by the constructor, and by `deposit` and `withdraw` alike — while
   `account.balance` keeps reading and assigning like an ordinary attribute.
   - A negative value raises `InvalidBalanceError` with the message
     `balance cannot be negative: -5`.
   - A value that is not an integer raises `InvalidBalanceError` with the message
     `balance must be a whole number of cents: '250'`.
   - A rejected assignment leaves the previous balance in place, so a withdrawal
     larger than the balance is refused and changes nothing.
3. `account_id` can be read but never reassigned: assigning to it raises
   `AttributeError`.
4. `Account.from_csv("A-7, Dana ,250")` builds an account from one comma-separated
   line of id, owner and balance. Surrounding spaces are dropped and the balance
   becomes an integer. Called on a subclass, it builds that subclass.
5. Everything `Account` already does must keep working, unchanged.

## Example

```python
account = Account.from_csv("A-7, Dana ,250")
account.withdraw(100)
print(account.balance)  # 150

account.balance = -5    # InvalidBalanceError: balance cannot be negative: -5
```

## Running the tests

From this folder: `python -m pytest`. `tests/test_requirements.py` is what scores;
`tests/test_existing.py` covers behavior that already works and must keep working.
