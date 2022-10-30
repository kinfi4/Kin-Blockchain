from time import time
from typing import Optional

from kin_blockchain.domain.entities import BlockIndex, BlockEntity, TransactionEntity
from kin_blockchain.domain.exceptions import TransactionInvalid, ProofValidationFailed
from kin_blockchain.domain.services import TransactionService, BlockService, WalletService


class Blockchain:
    def __init__(
        self,
        block_service: BlockService,
        transaction_service: TransactionService,
        wallet_service: WalletService,
    ) -> None:
        self._tr_service = transaction_service
        self._bl_service = block_service
        self._wallet_service = wallet_service

    def add_transaction(self, transaction: TransactionEntity) -> BlockIndex:
        if not transaction.is_valid():
            raise TransactionInvalid('Passed transaction is not valid')

        self._tr_service.add_transaction(transaction)

        return BlockIndex(self._bl_service.last_block.index + 1)

    def create_block(self, block: BlockEntity) -> BlockEntity:
        if not block.get_hash()[-2:] == "08":
            raise ProofValidationFailed(f'Could not create a block with {block.nonce=}, nonce did not pass validation')

        self._tr_service.flush_transactions()
        new_block = self._bl_service.add_block(block)

        self._transfer_previous_transactions()

        return new_block

    def validate_proof(self, nonce: int) -> tuple[bool, Optional[BlockEntity]]:
        block_to_hash = BlockEntity(
            index=BlockIndex(self._bl_service.last_block.index + 1),
            timestamp=time(),
            previous_block_hash=self._bl_service.last_block.get_hash(),
            transactions=self._tr_service.get_transactions(),
            nonce=nonce,
        )
        hash_result = block_to_hash.get_hash()
        nonce_check_result = hash_result[-2:] == "08"

        return nonce_check_result, block_to_hash if nonce_check_result else None

    def get_blockchain(self) -> list[BlockEntity]:
        return self._bl_service.get_blockchain()

    def _transfer_previous_transactions(self) -> None:
        transactions = self._bl_service.get_block(BlockIndex(self._bl_service.last_block.index - 1)).transactions

        for transaction in transactions:
            self._wallet_service.make_transaction(
                from_user_id=transaction.sender,
                to_user_id=transaction.receiver,
                amount=transaction.amount,
            )
