from time import time
from uuid import uuid4
from random import randint

from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.domain.entities.block import BlockEntity, BlockIndex
from kin_blockchain.domain.entities.transaction import TransactionEntity
from kin_blockchain.domain.services import BlockService, TransactionService


def create_genesis_block() -> BlockEntity:
    return BlockEntity(
        index=BlockIndex(0),
        previous_block_hash='makarov',
        timestamp=time(),
        transactions=[],
        proof=3082002
    )


def init_blockchain() -> Blockchain:
    genesis_block = create_genesis_block()
    block_service = BlockService([genesis_block])

    transaction_service = TransactionService()

    bc = Blockchain(block_service=block_service, transaction_service=transaction_service)

    return bc


def find_proof(bc: Blockchain) -> int:
    n = 0
    while not bc.validate_proof(n):
        n += 1

    return n


def build_dump_transaction() -> TransactionEntity:
    return TransactionEntity(
        receiver=uuid4().hex,
        sender=uuid4().hex,
        amount=randint(10, 10000),
    )


def create_block_in_blockchain(bc: Blockchain, transactions_amount: int) -> None:
    transactions = [build_dump_transaction() for _ in range(transactions_amount)]

    for tr in transactions:
        bc.add_transaction(tr)

    proof = find_proof(bc)

    bc.create_block(proof)


if __name__ == '__main__':
    blockchain = init_blockchain()

    create_block_in_blockchain(blockchain, 10)
    create_block_in_blockchain(blockchain, 8)
    create_block_in_blockchain(blockchain, 12)

    blocks = blockchain.get_blockchain()

    for block in blocks:
        print(block.previous_block_hash, end=' -> ')

    print('...')
