from time import time

from kin_blockchain.domain.entities import BlockEntity, BlockIndex


def mine_genesis_block() -> BlockEntity:
    n = 0

    while True:
        genesis_block = BlockEntity(
            index=BlockIndex(0),
            timestamp=time(),
            previous_block_hash='00000000000000',
            transactions=[],
            nonce=n,
        )

        hash_result = genesis_block.get_hash()
        if hash_result[-2:] == "08":
            break

    return genesis_block
