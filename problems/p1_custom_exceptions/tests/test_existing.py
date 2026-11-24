import pytest

from payments.processor import Account, PaymentProcessor

pytestmark = pytest.mark.guard


class RecordingGateway:
    def __init__(self):
        self.submitted = []

    def submit(self, account_id, amount):
        self.submitted.append((account_id, amount))


def make_processor(gateway=None, balance=50):
    processor = PaymentProcessor(gateway or RecordingGateway())
    processor.register(Account("A-1", balance))
    return processor


def test_successful_charge_returns_the_new_balance():
    assert make_processor(balance=50).charge("A-1", 20) == 30


def test_gateway_receives_the_charge():
    gateway = RecordingGateway()
    make_processor(gateway).charge("A-1", 20)
    assert gateway.submitted == [("A-1", 20)]


def test_non_positive_amount_raises_value_error():
    with pytest.raises(ValueError):
        make_processor().charge("A-1", 0)


def test_overdraw_raises_value_error_and_charges_nothing():
    gateway = RecordingGateway()
    with pytest.raises(ValueError):
        make_processor(gateway, balance=50).charge("A-1", 80)
    assert gateway.submitted == []
