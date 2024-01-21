from services.repositories.repository import Repository


class CSRFRepository(Repository):
    def __init__(self):
        super().__init__(
            "csrf",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "user_id": "INTEGER NOT NULL",
                "csrf": "TEXT NOT NULL",
            },
            {"user_id": "uspastb(id)"},
        )
