import random
import string

from app_settings import AppSettings
from services.aes_service import AESService
from services.hash_service import HashService
from services.repositories.csrf_repository import CSRFRepository

from utils.singleton import Singleton

from services.repositories.user_data_repository import UserDataRepository
from services.repositories.user_doc_repository import UserDocRepository
from services.repositories.user_pass_repository import UserPassRepository
from services.repositories.user_pepper_repository import UserPepperRepository


class UserService(Singleton):
    def __init__(self):
        self.pass_repository = UserPassRepository()
        self.data_repository = UserDataRepository()
        self.pepper_repository = UserPepperRepository()
        self.document_repository = UserDocRepository()
        self.csrf_repository = CSRFRepository()

        self.pass_repository.create_table()
        self.data_repository.create_table()
        self.pepper_repository.create_table()
        self.document_repository.create_table()
        self.csrf_repository.create_table()

    def does_user_exist(self, username):
        users_with_username = self.pass_repository.get("username", username)
        return len(users_with_username) > 0

    def does_email_exist(self, email):
        users_with_email = self.data_repository.get("email", email)
        return len(users_with_email) > 0

    def get_user_id_by_client_nr(self, client_nr):
        data = self.data_repository.get("client_nr", client_nr)
        return data[0]["user_id"] if len(data) > 0 else None

    def get_user_id_by_email(self, email):
        data = self.data_repository.get("email", email)
        return data[0]["user_id"] if len(data) > 0 else None

    def get_user_hidden_document(self, user_id):
        data = self.data_repository.get("user_id", user_id)
        return data[0]["document_nr"] if len(data) > 0 else None

    def get_user_document(self, user_id):
        document_nr = self.document_repository.get("user_id", user_id)[0]["document_nr"]
        return AESService().decrypt(document_nr)

    def get_user_client_nr(self, user_id):
        data = self.data_repository.get("user_id", user_id)
        return data[0]["client_nr"] if len(data) > 0 else None
    
    def get_user_email(self, user_id):
        data = self.data_repository.get("user_id", user_id)
        return data[0]["email"] if len(data) > 0 else None

    def verify_password(self, user_id, password):
        user_data = self.pass_repository.get("id", user_id)
        if len(user_data) <= 0:
            return None, False

        user_data = user_data[0]
        hash = user_data["hash"]
        pepper = self.pepper_repository.get("user_id", user_id)[0]["pepper"]
        return HashService().verify_password(password, hash, pepper)

    def login(self, username, password):
        users_with_username = self.pass_repository.get("username", username)
        if len(users_with_username) <= 0:
            return None, False

        user_data = users_with_username[0]
        user_id = user_data["id"] if user_data else None
        if user_id:
            hash = user_data["hash"]
            pepper = self.pepper_repository.get("user_id", user_id)[0]["pepper"]
            if HashService().verify_password(password, hash, pepper):
                return user_id, True
        return user_id, False

    def create_user(self, email, username, password, document_number):
        hash, pepper = HashService().hash_password(password)
        hidden_document_number = "*" * (len(document_number) - 3) + document_number[-3:]
        aes_document_number = AESService().encrypt(document_number)

        client_nr = "".join(
            random.choice(string.digits)
            for _ in range(AppSettings().get("client_nr_length"))
        )

        user_id = self.pass_repository.insert({"username": username, "hash": hash})
        self.pepper_repository.insert({"user_id": user_id, "pepper": pepper})
        self.data_repository.insert(
            {
                "user_id": user_id,
                "email": email,
                "document_nr": hidden_document_number,
                "client_nr": client_nr,
            }
        )
        self.document_repository.insert(
            {"user_id": user_id, "document_nr": aes_document_number}
        )
        return user_id

    def change_password(self, user_id, password):
        hash, pepper = HashService().hash_password(password)
        self.pass_repository.update({"hash": hash}, by="id", param=user_id)
        self.pepper_repository.update({"pepper": pepper}, by="user_id", param=user_id)
        return user_id

    def update_user(self, user_id, email, username, password):
        hash, pepper = HashService().hash_password(password)
        self.pass_repository.update(
            {"username": username, "hash": hash}, by="id", param=user_id
        )
        self.data_repository.update({"email": email}, by="user_id", param=user_id)
        self.pepper_repository.update({"pepper": pepper}, by="user_id", param=user_id)
        return user_id
    
    def set_csrf(self, user_id, csrf):
        if len(self.csrf_repository.get("user_id", user_id)) > 0:
            self.csrf_repository.update({"csrf": csrf}, by="user_id", param=user_id)
        else:
            self.csrf_repository.insert({"user_id": user_id, "csrf": csrf})

    def get_csrf(self, user_id):
        data = self.csrf_repository.get("user_id", user_id)
        return data[0]["csrf"] if len(data) > 0 else None
