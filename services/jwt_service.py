import datetime
from flask import current_app
import jwt
from app_settings import AppSettings

from utils.singleton import Singleton


class JWTService(Singleton):
    def encode(self, user_id, username, ip):
        return jwt.encode(
            {
                "user_id": user_id,
                "username": username,
                "ip": ip,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=AppSettings().get("auth_jwt_exp")),
            },
            current_app.config["SECRET_KEY"],
            "HS256",
        )

    def decode(self, token):
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
