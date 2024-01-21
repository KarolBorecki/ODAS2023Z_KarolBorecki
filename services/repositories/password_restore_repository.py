from services.repositories.repository import Repository


class PasswordRestoreRepository(Repository):
    def __init__(self):
        super().__init__(
            "passrestb",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "user_id": "INTEGER NOT NULL",
                "link": "INTEGER NOT NULL",
                "active": "INTEGER NOT NULL",
                "date_created": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            {"user_id": "uspastb(id)"},
        )
