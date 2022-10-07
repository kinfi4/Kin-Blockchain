from kin_blockchain.domain.entities import BlockEntity, BlockIndex


class BlockService:
    def __init__(self, genesis_block: BlockEntity) -> None:
        self._block_list = [genesis_block]

    def add_block(self, block: BlockEntity) -> BlockEntity:
        self._block_list.append(block)
        return block

    @property
    def last_block(self) -> BlockEntity:
        return self._block_list[-1]

    def get_block(self, block_idx: BlockIndex) -> BlockEntity:
        return self._block_list[block_idx]

    def get_blockchain(self) -> list[BlockEntity]:
        return self._block_list
