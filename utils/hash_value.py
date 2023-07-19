from passlib.hash import bcrypt


def hash_value(value: str) -> str:
    hashed = bcrypt.hash(value)
    return hashed
