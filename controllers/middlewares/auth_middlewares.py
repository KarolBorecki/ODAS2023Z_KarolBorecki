import datetime
from functools import wraps

from flask import redirect, request

from controllers.forms.login_form import LoginForm
from models.current_user import CurrentUser
from services.jwt_service import JWTService
from services.user_service import UserService


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.cookies:
            token = request.cookies["Authorization"]
            if not token:
                return redirect("/login")
            try:
                data = JWTService().decode(token)

                date = data["exp"]
                if date < datetime.datetime.utcnow().timestamp():
                    return redirect("/login")

                ip_addr = data["ip"]
                if ip_addr != request.remote_addr:
                    return redirect("/login")

                user_id = data["user_id"]
                username = data["username"]
                if UserService().does_user_exist(username):
                    current_user = CurrentUser(user_id, username)
                else:
                    return redirect("/login")
            except Exception as e:
                return redirect("/login")
        else:
            return redirect("/login")

        return f(current_user, *args, **kwargs)

    return decorator
