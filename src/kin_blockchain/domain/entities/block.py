import json
import hashlib
from dataclasses import dataclass
from typing import NewType, Optional, Any

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

    @classmethod
    def from_dict(cls, dtc: dict[str, Any]) -> "BlockEntity":
        return cls(
            index=BlockIndex(dtc['index']),
            previous_block_hash=dtc['previous_block_hash'],
            timestamp=dtc['timestamp'],
            transactions=[TransactionEntity.from_dict(dct_entity) for dct_entity in dtc['transactions']],
            nonce=dtc['nonce'],
        )
