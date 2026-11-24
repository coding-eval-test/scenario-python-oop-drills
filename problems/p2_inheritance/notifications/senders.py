"""The original e-mail sender. Other code still uses it - keep it working."""


class EmailSender:
    def __init__(self, sender_name, outbox):
        self.sender_name = sender_name
        self.outbox = outbox
        self.sent_count = 0

    def send(self, recipient, message):
        if not recipient or not message:
            raise ValueError("recipient and message are required")
        body = f"[{self.sender_name}] {message}"
        self.outbox.append(("email", recipient, body))
        self.sent_count += 1
        return body
