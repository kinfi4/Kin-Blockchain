from abc import ABC, abstractmethod

from kin_blockchain.domain.entities.wallet import WalletEntity


class IWalletRepository(ABC):
    @abstractmethod
    def get_user_balance(self, user_id: str) -> float:
        pass

    @abstractmethod
    def make_transaction(self, from_user_id: str, to_user_id: str, amount: float) -> None:
        pass

    @abstractmethod
    def get_all_wallets(self) -> list[WalletEntity]:
        pass

    @abstractmethod
    def is_transaction_valid(self, from_user_id: str, amount: float) -> bool:
        pass
