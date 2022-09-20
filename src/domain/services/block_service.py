from time import time

from src.domain.entities.block import Block, BlockIndex
from src.domain.entities.transaction import Transaction


class BlockService:
    def __init__(self, blocks_list: list[Block] = None) -> None:
        self._block_list = blocks_list if blocks_list else []

    def add_block(self, proof: int, transactions: list[Transaction]) -> Block:
        new_block_index = BlockIndex(len(self._block_list) + 1)
        block = Block(
            index=new_block_index,
            timestamp=time(),
            transactions=transactions,
            proof=proof,
            previous_block_hash=self.last_block.get_hash()
        )

        self._block_list.append(block)

        return block

    @property
    def last_block(self) -> Block:
        return self._block_list[-1]

    def get_block(self, block_idx: BlockIndex) -> Block:
        return self._block_list[block_idx]

    def get_blockchain(self) -> list[Block]:
        return self._block_list
