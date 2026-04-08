import hashlib
import hmac


def build_chatwoot_signature(*, secret: str, timestamp: str, raw_body: bytes) -> str:
    message = f"{timestamp}.".encode("utf-8") + raw_body
    digest = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def verify_chatwoot_signature(*, secret: str, timestamp: str, raw_body: bytes, received_signature: str) -> bool:
    expected = build_chatwoot_signature(secret=secret, timestamp=timestamp, raw_body=raw_body)
    return hmac.compare_digest(expected, received_signature)
