from kin_blockchain.constants import COINBASE_TRANSACTION_SENDER
from kin_blockchain.domain.entities.wallet import WalletEntity
from kin_blockchain.infrastructure.repositories.interfaces import IWalletRepository


class MemoryWalletRepository(IWalletRepository):
    def __init__(self):
        self._registry = {}

    def get_user_balance(self, user_id: str) -> float:
        if user_id not in self._registry:
            self._registry[user_id] = 0

        return self._registry[user_id]

    def is_transaction_valid(self, from_user_id: str, amount: float) -> bool:
        return from_user_id in self._registry and self._registry[from_user_id] >= amount

    def make_transaction(self, from_user_id: str, to_user_id: str, amount: float) -> None:
        if to_user_id not in self._registry:
            self._registry[to_user_id] = 0

        if from_user_id == COINBASE_TRANSACTION_SENDER:
            self._registry[to_user_id] += amount
            return

        if from_user_id not in self._registry:
            raise RuntimeError('Can not make transactions with unknown users')
        if self._registry[from_user_id] < amount:
            raise RuntimeError(f'Can make this transaction, {from_user_id} does not have enough tokens')

        transaction_passed = True
        initial_from_balance, initial_to_balance = self._registry[from_user_id], self._registry[to_user_id]

        try:
            self._registry[from_user_id] -= amount
            self._registry[to_user_id] += amount
        except Exception:
            transaction_passed = False
            raise
        finally:
            if not transaction_passed:
                self._registry[from_user_id] = initial_from_balance
                self._registry[to_user_id] = initial_to_balance

    def get_all_wallets(self) -> list[WalletEntity]:
        return [
            WalletEntity(user_id=wallet_tuple[0], balance=wallet_tuple[1])
            for wallet_tuple in self._registry.items()
        ]
