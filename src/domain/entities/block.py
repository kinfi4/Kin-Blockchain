import json
import hashlib
from dataclasses import dataclass
from typing import NewType

from src.domain.entities.transaction import Transaction


BlockIndex = NewType('BlockIndex', int)


@dataclass(frozen=True)
class Block:
    index: BlockIndex
    previous_block_hash: str
    timestamp: float
    proof: int
    transactions: list[Transaction]

    def get_hash(self) -> str:
        transaction_str = json.dumps(self.to_dict())
        return hashlib.sha224(transaction_str).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "previous_block_hash": self.previous_block_hash,
            "timestamp": self.timestamp,
            "proof": self.proof,
            "transactions": [transaction.to_dict() for transaction in self.transactions]
        }
