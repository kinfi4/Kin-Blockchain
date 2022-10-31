from kin_blockchain.domain.entities.transaction import TransactionEntity
from kin_blockchain.infrastructure.repositories import IWalletRepository


class TransactionService:
    def __init__(self, wallet_repository: IWalletRepository) -> None:
        self._transactions = []
        self._wallet_repository = wallet_repository

    def add_transaction(self, transaction: TransactionEntity) -> TransactionEntity:
        self._transactions.append(transaction)
        self._wallet_repository.add_tokens_to_frozen_state(transaction.sender, transaction.amount)

        return transaction

    def flush_transactions(self) -> list[TransactionEntity]:
        if not self._transactions:
            raise RuntimeError(f'Sorry but there are no transaction in the list!')

        transactions_to_return = self.get_transactions()
        self._transactions = []

        return transactions_to_return

    def get_transactions(self) -> list[TransactionEntity]:
        return self._transactions
