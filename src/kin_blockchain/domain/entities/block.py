import json
import hashlib
from dataclasses import dataclass
from typing import NewType, Optional

from kin_blockchain.domain.entities.transaction import TransactionEntity


BlockIndex = NewType('BlockIndex', int)


@dataclass
class BlockEntity:
    index: BlockIndex
    previous_block_hash: str
    timestamp: float
    transactions: list[TransactionEntity]
    nonce: Optional[int] = None

    def get_hash(self) -> str:
        if self.nonce is None:
            raise RuntimeError('Can not get hash of block without nonce')

        block_str = json.dumps(self.to_dict())
        return hashlib.sha256(block_str.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "previous_block_hash": self.previous_block_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "transactions": [transaction.to_dict() for transaction in self.transactions],
        }
