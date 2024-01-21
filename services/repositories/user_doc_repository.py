from services.repositories.repository import Repository


class UserDocRepository(Repository):
    def __init__(self):
        super().__init__(
            "doctb",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "user_id": "INTEGER NOT NULL",
                "document_nr": "TEXT NOT NULL",
            },
            {"user_id": "uspastb(id)"},
        )
