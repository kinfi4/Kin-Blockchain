from kin_blockchain.domain.entities.transaction import TransactionEntity


class TransactionService:
    def __init__(self) -> None:
        self._transactions = []

    def add_transaction(self, transaction: TransactionEntity) -> TransactionEntity:
        self._transactions.append(transaction)

        return transaction

    def flush_transactions(self) -> list[TransactionEntity]:
        if not self._transactions:
            raise RuntimeError(f'Sorry but there are no transaction in the list!')

        transactions_to_return = self.get_transactions()
        self._transactions = []

        return transactions_to_return

    def get_transactions(self) -> list[TransactionEntity]:
        return self._transactions
