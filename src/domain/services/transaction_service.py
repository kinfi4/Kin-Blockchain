from src.domain.entities.transaction import Transaction


class TransactionService:
    def __init__(self, transaction_list: list[Transaction] = None) -> None:
        self._transactions = transaction_list if transaction_list else []

    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def flush_transactions(self) -> list[Transaction]:
        if not self._transactions:
            raise RuntimeError(f'Sorry but there are no transaction in the list!')

        transactions_to_return = self._transactions
        self._transactions = []

        return transactions_to_return
