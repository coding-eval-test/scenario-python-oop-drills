"""Charges accounts through a payment gateway."""


class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance


class PaymentProcessor:
    def __init__(self, gateway):
        self._gateway = gateway
        self._accounts = {}

    def register(self, account):
        self._accounts[account.account_id] = account

    def charge(self, account_id, amount):
        """Take `amount` from the account and return the new balance."""
        if account_id not in self._accounts:
            raise Exception("account not found")
        account = self._accounts[account_id]
        if amount <= 0:
            raise ValueError("bad amount")
        if amount > account.balance:
            raise ValueError("insufficient funds")
        self._gateway.submit(account_id, amount)
        account.balance -= amount
        return account.balance
