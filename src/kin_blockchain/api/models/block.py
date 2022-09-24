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

    @classmethod
    def from_domain(cls, block_entity: BlockEntity) -> "BlockModel":
        return cls(
            index=block_entity.index,
            previous_block_hash=block_entity.previous_block_hash,
            timestamp=block_entity.timestamp,
            proof=block_entity.proof,
            transactions=[TransactionModel.from_domain(tr) for tr in block_entity.transactions],
        )
