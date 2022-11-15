import json
import hashlib
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TransactionEntity:
    sender: str
    receiver: str
    amount: float

    def get_hash(self) -> str:
        transaction_str = json.dumps(self.to_dict())
        return hashlib.sha224(transaction_str.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": float(self.amount),
        }

    def is_valid(self):
        return all([
            self.sender != '',
            self.receiver != '',
            self.amount > 0,
        ])

    @classmethod
    def from_dict(cls, dct: dict[str, Any]) -> "TransactionEntity":
        return cls(
            sender=dct['sender'],
            receiver=dct['receiver'],
            amount=dct['amount'],
        )
