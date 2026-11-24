import inspect

import pytest

from notifications.channels import (
    EmailNotifier,
    Notifier,
    SmsNotifier,
    UrgentEmailNotifier,
)


def test_notifier_is_abstract_and_cannot_be_instantiated():
    assert inspect.isabstract(Notifier)
    with pytest.raises(TypeError):
        Notifier("Ops", [])


def test_format_is_the_only_abstract_method():
    assert Notifier.__abstractmethods__ == frozenset({"format"})


def test_email_and_sms_are_notifiers():
    assert issubclass(EmailNotifier, Notifier)
    assert issubclass(SmsNotifier, Notifier)


def test_email_notifier_sends_a_formatted_message():
    outbox = []
    body = EmailNotifier("Ops", outbox).send("dana@example.com", "disk full")
    assert body == "[Ops] disk full"
    assert outbox == [("email", "dana@example.com", "[Ops] disk full")]


def test_sms_notifier_uses_its_own_channel_and_format():
    outbox = []
    body = SmsNotifier("Ops", outbox).send("+15550100", "disk full")
    assert body == "Ops: disk full"
    assert outbox == [("sms", "+15550100", "Ops: disk full")]


def test_sms_body_is_cut_to_160_characters():
    body = SmsNotifier("Ops", []).send("+15550100", "x" * 500)
    assert len(body) == 160
    assert body.startswith("Ops: xxx")


def test_send_lives_on_the_base_class_only():
    assert "send" in vars(Notifier)
    assert "send" not in vars(EmailNotifier)
    assert "send" not in vars(SmsNotifier)


def test_shared_send_validates_and_counts():
    notifier = SmsNotifier("Ops", [])
    notifier.send("+15550100", "one")
    notifier.send("+15550100", "two")
    assert notifier.sent_count == 2
    with pytest.raises(ValueError):
        notifier.send("", "three")
    assert notifier.sent_count == 2
    with pytest.raises(ValueError):
        notifier.send("+15550100", "")
    assert notifier.sent_count == 2


def test_urgent_notifier_builds_on_the_email_notifier():
    assert issubclass(UrgentEmailNotifier, EmailNotifier)
    outbox = []
    notifier = UrgentEmailNotifier("Ops", outbox)
    assert notifier.sender_name == "Ops"
    assert notifier.send("dana@example.com", "disk full") == "URGENT [Ops] disk full"
    assert outbox == [("email", "dana@example.com", "URGENT [Ops] disk full")]


def test_urgent_prefix_is_configurable():
    notifier = UrgentEmailNotifier("Ops", [], prefix="SEV1")
    assert notifier.prefix == "SEV1"
    assert notifier.send("dana@example.com", "disk full") == "SEV1 [Ops] disk full"
