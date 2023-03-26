import bcrypt


class Password:
    @classmethod
    def encrypt(cls, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @classmethod
    def is_valid(cls, given_password: str, expected_password: bytes) -> bool:
        return bcrypt.checkpw(given_password.encode("utf-8"), expected_password)
