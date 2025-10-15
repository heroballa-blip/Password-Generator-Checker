import hashlib
import base64

def derive_key(password):
    """
    Derive a 32-byte Fernet-compatible key from a password using SHA-256.
    """
    sha_hash = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(sha_hash)
