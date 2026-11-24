import pytest

from bank.account import Account, InvalidBalanceError


def test_invalid_balance_error_is_a_value_error():
    assert issubclass(InvalidBalanceError, ValueError)


def test_balance_is_a_managed_attribute():
    assert isinstance(vars(Account).get("balance"), property)


def test_negative_balance_is_rejected_and_the_old_value_kept():
    account = Account("A-7", "Dana", 100)
    with pytest.raises(InvalidBalanceError) as caught:
        account.balance = -5
    assert str(caught.value) == "balance cannot be negative: -5"
    assert account.balance == 100


def test_non_integer_balance_is_rejected():
    account = Account("A-7", "Dana", 100)
    with pytest.raises(InvalidBalanceError) as caught:
        account.balance = "250"
    assert str(caught.value) == "balance must be a whole number of cents: '250'"
    assert account.balance == 100


def test_constructor_validates_the_opening_balance():
    with pytest.raises(InvalidBalanceError):
        Account("A-7", "Dana", -1)


def test_overdrawing_is_rejected_and_the_balance_kept():
    account = Account("A-7", "Dana", 100)
    with pytest.raises(InvalidBalanceError):
        account.withdraw(500)
    assert account.balance == 100


def test_account_id_is_read_only():
    account = Account("A-7", "Dana", 100)
    with pytest.raises(AttributeError):
        account.account_id = "A-8"
    assert account.account_id == "A-7"


def test_from_csv_builds_an_account():
    account = Account.from_csv("A-7, Dana ,250")
    assert (account.account_id, account.owner, account.balance) == ("A-7", "Dana", 250)


def test_from_csv_builds_the_class_it_was_called_on():
    class SavingsAccount(Account):
        pass

    assert type(SavingsAccount.from_csv("S-1,Lee,900")) is SavingsAccount
