from dataclasses import dataclass


@dataclass
class WalletEntity:
    user_id: str
    balance: float
