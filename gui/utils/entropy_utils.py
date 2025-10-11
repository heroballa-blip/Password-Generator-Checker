import string
import math

def compute_entropy_from_text(password: str):
    """
    Estimate entropy based on character variety and length.
    - Letters, numbers, punctuation, and spaces are counted.
    """
    if not password:
        return 0.0

    sets = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
        " "  # treat space as separate set
    ]

    pool_size = 0
    for s in sets:
        if any(c in s for c in password):
            pool_size += len(s)

    if pool_size == 0:
        return 0.0

    return math.log2(pool_size) * len(password)

def adjusted_strength(password: str, dictionary: set[str]) -> tuple[str, float]:
    """
    Compute adjusted strength with partial word matching and repeated pattern detection.
    """
    text = password.lower()
    entropy = compute_entropy_from_text(password)

    # 1. Partial dictionary word penalty
    for word in dictionary:
        if len(word) >= 4 and word in text:
            entropy *= 0.6

    # 2. Repeated substring patterns penalty (length >=4)
    for length in range(4, min(12, len(password)//2 + 1)):  # check substrings 4-12 chars
        for i in range(len(password) - length + 1):
            substr = text[i:i+length]
            count = text.count(substr)
            if count > 1:
                entropy *= (0.8 ** (count-1))  # stronger penalty for more repeats

    # 3. Spaces penalty (human-readable sentence)
    if " " in password:
        entropy *= 0.5

    # 4. Classify strength
    if entropy < 72:
        return "Very Weak", entropy
    elif entropy < 100:
        return "Weak", entropy
    elif entropy < 128:
        return "Medium", entropy
    elif entropy < 175:
        return "Strong", entropy
    else:
        return "Very Strong", entropy