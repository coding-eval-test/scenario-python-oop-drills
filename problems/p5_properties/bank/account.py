"""A bank account. Balances are whole cents."""


class InvalidBalanceError:
    """Placeholder so the tests can import it - see PROBLEM.md."""


class Account:
    def __init__(self, account_id, owner, balance=0):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance

    def deposit(self, cents):
        self.balance += cents

    def withdraw(self, cents):
        self.balance -= cents

    def summary(self):
        return f"{self.account_id} {self.owner}: {self.balance}"
