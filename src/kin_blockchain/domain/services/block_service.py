from time import time

from kin_blockchain.domain.entities.block import BlockEntity, BlockIndex
from kin_blockchain.domain.entities.transaction import TransactionEntity


class BlockService:
    def __init__(self, genesis_block: BlockEntity = None) -> None:
        self._block_list = [genesis_block] if genesis_block else [self.generate_genesis_block()]

    def add_block(self, proof: int, transactions: list[TransactionEntity]) -> BlockEntity:
        new_block_index = BlockIndex(self.last_block.index + 1)
        block = BlockEntity(
            index=new_block_index,
            timestamp=time(),
            transactions=transactions,
            proof=proof,
            previous_block_hash=self.last_block.get_hash()
        )

        self._block_list.append(block)

        return block

    @property
    def last_block(self) -> BlockEntity:
        return self._block_list[-1]

    def get_block(self, block_idx: BlockIndex) -> BlockEntity:
        return self._block_list[block_idx]

    def get_blockchain(self) -> list[BlockEntity]:
        return self._block_list

    @staticmethod
    def generate_genesis_block() -> BlockEntity:
        return BlockEntity(
            index=BlockIndex(0),
            previous_block_hash='makarov',
            timestamp=time(),
            transactions=[],
            proof=3082002
        )
