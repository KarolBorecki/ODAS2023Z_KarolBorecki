import datetime
from app_settings import AppSettings
from services.repositories.tries_repository import TriesRepository
from utils.datetime_utils import get_date_from_str
from utils.singleton import Singleton


class TriesService(Singleton):
    def __init__(self):
        self.repository = TriesRepository()
        self.repository.create_table()

    def add(self, user_id, ip):
        return self.repository.insert({"user_id": user_id, "ip": ip, "sucess": 0})

    def make_sucess(self, id):
        return self.repository.update({"sucess": 1}, "id", id)

    def get_tries(
        self, user_id, time_in_minutes=AppSettings().get("auth_tries_timeout")
    ):
        tries_for_user = self.repository.get("user_id", user_id)
        tries_for_user = sorted(
            tries_for_user, key=lambda d: get_date_from_str(d["date"]), reverse=True
        )
        return list(
            filter(
                lambda d: datetime.datetime.utcnow().timestamp()
                - get_date_from_str(d["date"]).timestamp()
                <= time_in_minutes * 60,
                tries_for_user,
            )
        )

    def get_failed_tries_count(self, user_id, time_in_minutes=60):
        tries = self.get_tries(user_id, time_in_minutes)
        count = 0
        for t in tries:
            if t["sucess"] == 0:
                count += 1
            else:
                break
        return count

    def make_last_login_sucess(self, user_id, ip):  # NOT TESTED
        tries_data = self.repository.get("user_id", user_id)
        if len(tries_data) == 0:
            return False
        last_login_ip = sorted(tries_data, key=lambda d: get_date_from_str(d["date"]))[
            0
        ]["id"]
        self.repository.update({"sucess": 1}, "id", last_login_ip)
