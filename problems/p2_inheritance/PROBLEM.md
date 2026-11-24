# P2 — Inheritance and abstract bases

**Suggested time:** 15 minutes · **Worth:** 20 points

## Context

`notifications/senders.py` has one class, `EmailSender`, that validates a message,
formats it, records it, and counts it. The team now needs text messages and urgent
e-mails too, and does not want that logic copied into every new class.
`notifications/channels.py` holds placeholder classes for the new design.

## Requirements

1. `Notifier` is the shared base class. It is built with `(sender_name, outbox)` and
   keeps `sender_name`, `outbox`, and a `sent_count` that starts at 0.
2. `Notifier` is an abstract base class. It cannot be used on its own: creating one
   raises `TypeError`, and so does creating any subclass that does not supply
   `format(message)`. `format` is its one abstract method — the one thing every channel
   must supply — and it returns the text that channel delivers.
3. `send(recipient, message)` is written once, on `Notifier`, and no channel redefines
   it. It raises `ValueError` when the recipient or the message is empty; otherwise it
   appends `(channel, recipient, body)` to the outbox, adds one to `sent_count`, and
   returns the body.
4. `EmailNotifier` is a `Notifier` whose channel is `"email"` and whose body reads
   `[Ops] disk full` for sender `Ops`.
5. `SmsNotifier` is a `Notifier` whose channel is `"sms"` and whose body reads
   `Ops: disk full`, cut to at most 160 characters.
6. `UrgentEmailNotifier` is an `EmailNotifier` that takes an optional `prefix`
   (default `"URGENT"`), keeps it as `prefix`, and puts it in front of the normal
   e-mail body: `URGENT [Ops] disk full`.
7. `EmailSender` is still used elsewhere. It must keep working, unchanged.

## Example

```python
outbox = []
SmsNotifier("Ops", outbox).send("+15550100", "disk full")
UrgentEmailNotifier("Ops", outbox, prefix="SEV1").send("dana@example.com", "disk full")

print(outbox)
# [('sms', '+15550100', 'Ops: disk full'),
#  ('email', 'dana@example.com', 'SEV1 [Ops] disk full')]
```

## Running the tests

From this folder: `python -m pytest`. `tests/test_requirements.py` is what scores;
`tests/test_existing.py` covers behavior that already works and must keep working.
