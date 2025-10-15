from argon2.low_level import hash_secret_raw, Type
import os
import base64
from typing import Optional, Tuple

def derive_key(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(16)  # 128-bit salt

    key = hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=3,        # iterations (increase for more security)
        memory_cost=65536,  # in KB (64 MB)
        parallelism=2,
        hash_len=32,        # length of key in bytes
        type=Type.ID        # Argon2id
    )

    return base64.urlsafe_b64encode(key), salt
