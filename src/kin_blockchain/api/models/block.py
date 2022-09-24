from pydantic import BaseModel

from kin_blockchain.domain.entities import BlockIndex, BlockEntity
from kin_blockchain.api.models import TransactionModel


class BlockModel(BaseModel):
    index: BlockIndex
    previous_block_hash: str
    timestamp: float
    proof: int
    transactions: list[TransactionModel]

    def to_domain(self) -> BlockEntity:
        return BlockEntity(
            index=self.index,
            previous_block_hash=self.previous_block_hash,
            timestamp=self.timestamp,
            proof=self.proof,
            transactions=[tr.to_domain() for tr in self.transactions]
        )
