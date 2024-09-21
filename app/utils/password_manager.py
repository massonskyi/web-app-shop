import os
from passlib.context import CryptContext

__all__ = [
    'PasswordManager',
]


class PasswordManager:
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    def __init__(self) -> None:
        self.secret_key = os.urandom(32)

    def hash(self, pwd: str) -> str:
        return self.pwd_context.hash(pwd)

    def verify(self, hashed_password: str, plain_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


    def is_hashed(self, password: str) -> bool:
        # Passlib's identify method will return None if it cannot identify the hash scheme
        return self.pwd_context.identify(password) is not None
    
if __name__ == "__main__":
    pwds = "password"
    pwd = PasswordManager()
    hashed_pwd = pwd.hash(pwds)
    print(hashed_pwd)
    print(pwd.verify(hashed_pwd, pwds))
    print(pwd.verify(hashed_pwd, "wrong_password"))
