from services.repositories.repository import Repository


class UserPepperRepository(Repository):
    def __init__(self):
        super().__init__(
            "peptb",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "user_id": "INTEGER NOT NULL",
                "pepper": "TEXT NOT NULL",
            },
            {"user_id": "uspastb(id)"},
        )
