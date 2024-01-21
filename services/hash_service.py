import random
import string
from passlib.hash import sha256_crypt
from app_settings import AppSettings


from utils.singleton import Singleton


class HashService(Singleton):
    def __init__(self):
        super().__init__()

    def get_pepper(self):
        return "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(AppSettings().get("auth_pepper_length"))
        )

    def hash_password(self, password):
        pepper = self.get_pepper()
        password = password + pepper
        return (
            sha256_crypt.hash(password, rounds=AppSettings().get("auth_hash_rounds")),
            pepper,
        )

    def verify_password(self, password, hash, pepper):
        return sha256_crypt.verify(password + pepper, hash)

    def generate_password(self, length):
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )
    
    def generate_csrf_token(self):
        return self.generate_password(32)
