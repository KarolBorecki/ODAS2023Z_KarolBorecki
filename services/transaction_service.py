from services.repositories.transaction_repository import TransactionsRepository
from utils.singleton import Singleton


class TransactionService(Singleton):
    def __init__(self):
        self.repository = TransactionsRepository()

        self.repository.create_table()

    def new(self, title, from_id, to_id, value):
        return self.repository.insert(
            {"title": title, "from_id": from_id, "to_id": to_id, "value": value}
        )

    def get_incomes(self, user_id):
        return self.repository.get(by="to_id", param=user_id)

    def get_expenses(self, user_id):
        return self.repository.get(by="from_id", param=user_id)
