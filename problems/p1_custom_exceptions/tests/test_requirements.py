import pytest

from payments.errors import (
    AccountNotFoundError,
    GatewayError,
    InsufficientFundsError,
    InvalidAmountError,
    PaymentError,
)
from payments.processor import Account, PaymentProcessor


class RecordingGateway:
    def submit(self, account_id, amount):
        pass


class DownGateway:
    def __init__(self):
        self.failure = ConnectionError("gateway unreachable")

    def submit(self, account_id, amount):
        raise self.failure


def make_processor(gateway=None, balance=50):
    processor = PaymentProcessor(gateway or RecordingGateway())
    processor.register(Account("A-1", balance))
    return processor


def test_payment_error_is_an_exception():
    assert issubclass(PaymentError, Exception)


def test_every_specific_error_is_a_payment_error():
    for error in (AccountNotFoundError, InvalidAmountError, InsufficientFundsError, GatewayError):
        assert issubclass(error, PaymentError)


def test_amount_and_funds_errors_are_still_value_errors():
    assert issubclass(InvalidAmountError, ValueError)
    assert issubclass(InsufficientFundsError, ValueError)


def test_unknown_account_raises_account_not_found():
    with pytest.raises(AccountNotFoundError) as caught:
        make_processor().charge("nope", 10)
    assert caught.value.account_id == "nope"


def test_account_not_found_message():
    with pytest.raises(AccountNotFoundError) as caught:
        make_processor().charge("nope", 10)
    assert str(caught.value) == "Account 'nope' not found"


def test_non_positive_amount_raises_invalid_amount():
    with pytest.raises(InvalidAmountError) as caught:
        make_processor().charge("A-1", -5)
    assert caught.value.amount == -5
    assert str(caught.value) == "Amount must be positive, got -5"


def test_overdraw_raises_insufficient_funds_with_details():
    with pytest.raises(InsufficientFundsError) as caught:
        make_processor(balance=50).charge("A-1", 80)
    assert caught.value.account_id == "A-1"
    assert caught.value.balance == 50
    assert caught.value.requested == 80


def test_insufficient_funds_shortfall_and_message():
    with pytest.raises(InsufficientFundsError) as caught:
        make_processor(balance=50).charge("A-1", 80)
    assert caught.value.shortfall == 30
    assert str(caught.value) == "Account 'A-1' has 50 but 80 was requested"


def test_gateway_failure_is_wrapped_and_chained():
    gateway = DownGateway()
    account = Account("A-1", 50)
    processor = PaymentProcessor(gateway)
    processor.register(account)
    with pytest.raises(GatewayError) as caught:
        processor.charge("A-1", 10)
    assert caught.value.__cause__ is gateway.failure
    assert caught.value.account_id == "A-1"
    assert account.balance == 50
