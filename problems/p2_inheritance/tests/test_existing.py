import pytest

from notifications.senders import EmailSender

pytestmark = pytest.mark.guard


def test_email_sender_formats_and_records_the_message():
    outbox = []
    body = EmailSender("Ops", outbox).send("dana@example.com", "disk full")
    assert body == "[Ops] disk full"
    assert outbox == [("email", "dana@example.com", "[Ops] disk full")]


def test_email_sender_counts_what_it_sent():
    sender = EmailSender("Ops", [])
    sender.send("dana@example.com", "one")
    sender.send("dana@example.com", "two")
    assert sender.sent_count == 2


def test_email_sender_rejects_an_empty_recipient_or_message():
    sender = EmailSender("Ops", [])
    with pytest.raises(ValueError):
        sender.send("", "hello")
    with pytest.raises(ValueError):
        sender.send("dana@example.com", "")
    assert sender.sent_count == 0
