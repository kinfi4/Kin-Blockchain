from time import time

from kin_blockchain.domain.entities import BlockEntity, BlockIndex, TransactionEntity


def mine_genesis_block() -> BlockEntity:
    n = 0

    while True:
        genesis_block = BlockEntity(
            index=BlockIndex(0),
            timestamp=time(),
            previous_block_hash='00000000000000',
            transactions=[
                # TransactionEntity(
                #     sender='00000',
                #     receiver='00000',
                #     amount=3.0,
                # )
            ],
            nonce=n,
        )

        hash_result = genesis_block.get_hash()
        if hash_result[-2:] == "08":
            break

    return genesis_block
