from kin_blockchain.constants import COINBASE_TRANSACTION_SENDER
from kin_blockchain.domain.entities import WalletEntity
from kin_blockchain.domain.exceptions import TransactionInvalid
from kin_blockchain.infrastructure.repositories.interfaces import IWalletRepository


class WalletService:
    def __init__(self, wallet_repository: IWalletRepository):
        self._wallet_repository = wallet_repository

    def get_user_wallet(self, user_id: str) -> WalletEntity:
        return WalletEntity(
            user_id=user_id,
            balance=self._wallet_repository.get_user_balance(user_id=user_id)
        )

    def is_transaction_valid(self, from_user_id: str, amount: float) -> bool:
        return self._wallet_repository.is_transaction_valid(from_user_id, amount) or self._is_coinbase_transaction(from_user_id)

    def make_transaction(self, from_user_id: str, to_user_id: str, amount: float):
        if not self.is_transaction_valid(from_user_id, amount):
            raise TransactionInvalid(f'User {from_user_id} does not have enough tokes to make transaction')

        # try:
        self._wallet_repository.make_transaction(from_user_id, to_user_id, amount)
        # except Exception:
        #     raise TransactionInvalid('Something went wrong!')

    def get_all_wallets(self) -> list[WalletEntity]:
        return self._wallet_repository.get_all_wallets()

    @staticmethod
    def _is_coinbase_transaction(from_user_id: str) -> bool:
        return from_user_id == COINBASE_TRANSACTION_SENDER
