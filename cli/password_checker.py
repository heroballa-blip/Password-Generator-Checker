import string
import math
import os
import getpass
from cli_utils import CancelOperation, QuitProgram

def calculate_entropy(length, exclude):
    pool_size = len(string.ascii_letters + string.digits)
    if not exclude:
        pool_size += len(string.punctuation)
    return round(length * math.log2(pool_size), 2)

def strength_rating(entropy):
    if entropy < 90:
        return "Weak"
    elif entropy < 180:
        return "Medium"
    else:
        return "Strong"

def get_dictionary_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    return os.path.join(root_dir, "resources", "dictionary.txt")

def load_dictionary(path=None):
    if path is None:
        path = get_dictionary_path()
    words = set()
    if not os.path.exists(path):
        print(f"Dictionary file not found at: {path}")
        return words
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            w = line.strip().lower()
            if len(w) >= 3:
                words.add(w)
    return words

def check_dictionary_match(password, dict_words):
    pw_lower = password.lower()
    matches = []
    for word in dict_words:
        if word in pw_lower:
            match_type = "full" if pw_lower == word else "partial"
            matches.append((word, match_type))
    return matches

DICT_WORDS = load_dictionary()

def checker():
    try:
        password = getpass.getpass("Enter your password to check its entropy: ")
        if password.strip().lower() in ("x", "q"):
            raise QuitProgram()
    except (CancelOperation, QuitProgram):
        raise

    length = len(password)
    exclude = all(char.isalnum() for char in password)
    base_entropy = calculate_entropy(length, exclude)
    matches = check_dictionary_match(password, DICT_WORDS)

    penalty = 0
    if matches:
        print()
        for word, match_type in matches:
            word_penalty = len(word) * (2 if match_type == "full" else 1)
            penalty += word_penalty
            print(f"Dictionary {match_type} match found: '{word}' → -{word_penalty} bits")

    adjusted_entropy = max(0, base_entropy - penalty)

    print(f"\nPassword Length: {length}")
    print(f"Base Entropy: {base_entropy} bits")
    print(f"Adjusted Entropy: {adjusted_entropy} bits")
    print(f"Strength: {strength_rating(adjusted_entropy)}")
