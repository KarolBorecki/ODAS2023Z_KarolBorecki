import json
from utils.singleton import Singleton


class AppSettings(Singleton):
    def __init__(self) -> None:
        super().__init__()

        with open("appsettings.json", "r") as jsonfile:
            self.data = json.load(jsonfile)
            jsonfile.close()

    def get(self, key):
        return self.data[key]
