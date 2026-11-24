import pytest

from bank.account import Account

pytestmark = pytest.mark.guard


def test_new_account_defaults_to_a_zero_balance():
    assert Account("A-7", "Dana").balance == 0


def test_deposit_adds_to_the_balance():
    account = Account("A-7", "Dana", 100)
    account.deposit(50)
    assert account.balance == 150


def test_withdraw_takes_from_the_balance():
    account = Account("A-7", "Dana", 100)
    account.withdraw(40)
    assert account.balance == 60


def test_summary_names_the_account_owner_and_balance():
    assert Account("A-7", "Dana", 100).summary() == "A-7 Dana: 100"
