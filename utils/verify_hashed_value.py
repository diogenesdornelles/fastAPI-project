from passlib.hash import bcrypt


def verify_hashed_value(password: str, hashed_password: str) -> bool:
    is_valid = bcrypt.verify(password, hashed_password)
    return is_valid
