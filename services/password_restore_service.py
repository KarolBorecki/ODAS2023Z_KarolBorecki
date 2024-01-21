import datetime
from app_settings import AppSettings
from services.hash_service import HashService
from services.repositories.password_restore_repository import PasswordRestoreRepository
from utils.datetime_utils import get_date_from_str
from utils.singleton import Singleton


class PasswordRestoreService(Singleton):
    def __init__(self):
        self.repository = PasswordRestoreRepository()

        self.repository.create_table()

    def new_restore_link(self, user_id):
        link = HashService().generate_password(32)
        self.repository.insert({"user_id": user_id, "link": link, "active": 1})
        return link

    def get_user_id_by_restore_link(self, restore_link):
        data = self.repository.get(by="link", param=restore_link)
        if len(data) <= 0:
            return None
        data = data[0]
        elapsed_time_min = (
            datetime.datetime.utcnow().timestamp()
            - get_date_from_str(data["date_created"]).timestamp()
        ) / 60
        if (
            elapsed_time_min > AppSettings().get("password_restore_timeout")
            or data["active"] == 0
        ):
            return None

        return data["user_id"] if len(data) > 0 else None

    def use_restore_link(self, restore_link):
        self.repository.update({"active": 0}, by="link", param=restore_link)
        return HashService().generate_password(
            AppSettings().get("password_restore_length")
        )
