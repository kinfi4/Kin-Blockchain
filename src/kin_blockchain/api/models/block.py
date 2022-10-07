from pydantic import BaseModel

from kin_blockchain.domain.entities import BlockIndex, BlockEntity
from kin_blockchain.api.models import TransactionModel


class BlockModel(BaseModel):
    index: BlockIndex
    previous_block_hash: str
    timestamp: float
    nonce: int
    transactions: list[TransactionModel]
    hash: str

    def to_domain(self) -> BlockEntity:
        return BlockEntity(
            index=self.index,
            previous_block_hash=self.previous_block_hash,
            timestamp=self.timestamp,
            nonce=self.nonce,
            transactions=[tr.to_domain() for tr in self.transactions]
        )

    @classmethod
    def from_domain(cls, block_entity: BlockEntity) -> "BlockModel":
        return cls(
            index=block_entity.index,
            previous_block_hash=block_entity.previous_block_hash,
            timestamp=block_entity.timestamp,
            nonce=block_entity.nonce,
            transactions=[TransactionModel.from_domain(tr) for tr in block_entity.transactions],
            hash=block_entity.get_hash(),
        )
