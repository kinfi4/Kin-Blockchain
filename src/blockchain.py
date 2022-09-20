import hashlib

from src.domain.entities.block import BlockIndex, Block
from src.domain.entities.transaction import Transaction
from src.domain.exceptions import TransactionInvalid, ProofValidationFailed
from src.domain.services import TransactionService, BlockService


class Blockchain:
    def __init__(self, block_service: BlockService, transaction_service: TransactionService):
        self._tr_service = transaction_service
        self._bl_service = block_service

    def add_transaction(self, transaction: Transaction) -> BlockIndex:
        if not transaction.is_valid():
            raise TransactionInvalid('Passed transaction is not valid')

        self._tr_service.add_transaction(transaction)

        return BlockIndex(self._bl_service.last_block.index + 1)

    def create_block(self, proof: int) -> Block:
        if not self.validate_proof(proof):
            raise ProofValidationFailed(f'Could not create a block with {proof=}, proof did not pass validation')

        transactions = self._tr_service.flush_transactions()

        return self._bl_service.add_block(proof, transactions)

    def validate_proof(self, proof: int) -> bool:
        last_block_proof = self._bl_service.last_block.proof

        to_hash = f'{last_block_proof}{proof}'.encode()
        hash_result = hashlib.sha256(to_hash).hexdigest()

        return hash_result[-2:] == "08"

    def get_blockchain(self) -> list[Block]:
        return self._bl_service.get_blockchain()
