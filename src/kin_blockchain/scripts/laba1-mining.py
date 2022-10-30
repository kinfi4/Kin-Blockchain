from uuid import uuid4
from random import randint

from kin_blockchain.api.mining_service import MiningService
from kin_blockchain.domain.services import BlockService, TransactionService
from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.domain.utils import mine_genesis_block
from kin_blockchain.domain.entities import TransactionEntity


def init_blockchain() -> Blockchain:
    block_service = BlockService(genesis_block=mine_genesis_block())

    transaction_service = TransactionService()

    bc = Blockchain(block_service=block_service, transaction_service=transaction_service)

    return bc


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

    block = mine_service.mine_new_block()
    bc.create_block(block)


if __name__ == '__main__':
    blockchain = init_blockchain()
    mine_service = MiningService(blockchain)

    create_block_in_blockchain(blockchain, 10)
    create_block_in_blockchain(blockchain, 8)
    create_block_in_blockchain(blockchain, 12)

    blocks = blockchain.get_blockchain()

    for b in blocks:
        print(b.previous_block_hash, end=' -> ')

    print('...')
