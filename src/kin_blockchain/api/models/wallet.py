from pydantic import BaseModel

from kin_blockchain.domain.entities import WalletEntity


class WalletModel(BaseModel):
    user_id: str
    balance: float

    @classmethod
    def from_domain(cls, domain_wallet: WalletEntity) -> 'WalletModel':
        return cls(
            user_id=domain_wallet.user_id,
            balance=domain_wallet.balance,
        )
