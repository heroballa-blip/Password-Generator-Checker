import string
import secrets

def generate_password(
    length: int = 16,
    exclude_special: bool = False,
    exclude_numbers: bool = False,
    exclude_letters: bool = False
):
    """Generate a random password"""
    if length < 16:
        raise ValueError("Password length must be at least 16 characters")

    chars = ""
    if not exclude_letters:
        chars += string.ascii_letters
    if not exclude_numbers:
        chars += string.digits
    if not exclude_special:
        chars += string.punctuation

    if not chars:
        return ""

    return "".join(secrets.choice(chars) for _ in range(length))
