import json
import hashlib
from dataclasses import dataclass
from typing import NewType

from kin_blockchain.domain.entities.transaction import TransactionEntity


BlockIndex = NewType('BlockIndex', int)


@dataclass(frozen=True)
class BlockEntity:
    index: BlockIndex
    previous_block_hash: str
    timestamp: float
    proof: int
    transactions: list[TransactionEntity]

    def get_hash(self) -> str:
        transaction_str = json.dumps(self.to_dict())
        return hashlib.sha224(transaction_str.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "previous_block_hash": self.previous_block_hash,
            "timestamp": self.timestamp,
            "proof": self.proof,
            "transactions": [transaction.to_dict() for transaction in self.transactions]
        }
