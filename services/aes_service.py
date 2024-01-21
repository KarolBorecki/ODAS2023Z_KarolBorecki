import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from flask import current_app

from utils.singleton import Singleton


class AESService(Singleton):
    def __init__(self):
        self.bs = AES.block_size
        key = current_app.config["AES_SECRET_KEY"]
        self.key = hashlib.sha256(
            key.encode()
        ).digest()  # 32 bytes, ensures stabillity of the key no matter what we put there

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode("utf-8")

    def decrypt(self, enc):  # TODO not working
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESService._unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]
