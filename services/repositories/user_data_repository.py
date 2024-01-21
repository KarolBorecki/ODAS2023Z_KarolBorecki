from services.repositories.repository import Repository


class UserDataRepository(Repository):
    def __init__(self):
        super().__init__(
            "usdatb",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "user_id": "INTEGER NOT NULL",
                "email": "TEXT NOT NULL",
                "client_nr": "TEXT NOT NULL",
                "document_nr": "TEXT NOT NULL",
            },
            {"user_id": "uspastb(id)"},
        )
