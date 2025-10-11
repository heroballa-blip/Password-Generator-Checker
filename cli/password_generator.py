import secrets
import string
from cli_utils import prompt, CancelOperation, QuitProgram

def prompt_length():
    while True:
        try:
            raw = prompt("Choose password length (Minimum is 16): ")
            length = int(raw.strip())
            if length >= 16:
                return length
            print(f"{length} characters not enough. Try again.")
        except ValueError:
            print("Invalid choice. Type a number.")
        except (CancelOperation, QuitProgram):
            raise

def exclude_special_char():
    while True:
        try:
            choice = prompt("Exclude special characters? (y/n): ").lower().strip()
            if choice in ['y', 'n']:
                return choice == 'y'
            print("Invalid choice. Please enter 'y' or 'n'.")
        except (CancelOperation, QuitProgram):
            raise

def generate_password(length, exclude):
    char_pool = string.ascii_letters + string.digits
    must_have = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits)
    ]
    if not exclude:
        char_pool += string.punctuation
        must_have.append(secrets.choice(string.punctuation))

    if length < len(must_have):
        raise ValueError("Length too short for required character types.")

    password = must_have + [secrets.choice(char_pool) for _ in range(length - len(must_have))]
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)
