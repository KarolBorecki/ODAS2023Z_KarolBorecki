from services.repositories.repository import Repository


class UserPassRepository(Repository):
    def __init__(self):
        super().__init__(
            "uspastb",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "username": "TEXT NOT NULL",
                "hash": "TEXT NOT NULL",
                "date_created": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            {},
        )
