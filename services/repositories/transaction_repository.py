from services.repositories.repository import Repository


class TransactionsRepository(Repository):
    def __init__(self):
        super().__init__(
            "trtb",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "title": "TEXT NOT NULL",
                "from_id": "INTEGER NOT NULL",
                "to_id": "INTEGER NOT NULL",
                "value": "INTEGER NOT NULL",
                "date_created": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            {"from_id": "uspastb(id)", "to_id": "uspastb(id)"},
        )
