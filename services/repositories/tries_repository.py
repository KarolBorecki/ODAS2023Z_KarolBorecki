from services.repositories.repository import Repository


class TriesRepository(Repository):
    def __init__(self):
        super().__init__(
            "logfromtb",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "user_id": "INTEGER NOT NULL",
                "ip": "INTEGER NOT NULL",
                "date": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "sucess": "INTEGER NOT NULL",
            },
            {"user_id": "uspastb(id)"},
        )
