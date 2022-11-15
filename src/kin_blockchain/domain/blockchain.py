from time import time
from typing import Optional
from urllib.parse import urlparse

import requests

from kin_blockchain.constants import IS_LOCAL
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
        self._registered_nodes = set()
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
        transactions = self._bl_service.get_block(BlockIndex(self._bl_service.last_block.index)).transactions

        for transaction in transactions:
            self._wallet_service.make_transaction(
                from_user_id=transaction.sender,
                to_user_id=transaction.receiver,
                amount=transaction.amount,
            )

    def resolve_conflicts(self) -> bool:
        max_chain_length = len(self._bl_service.get_blockchain())
        exchanged_blockchain = False

        for host in self._registered_nodes:
            blockchain_url = f'http://{host}/api/blocks/full-blockchain'
            blocks = requests.get(blockchain_url).json()

            block_entities = [BlockEntity.from_dict(block) for block in blocks]

            if len(blocks) > max_chain_length and self._is_chain_valid(block_entities):
                self._bl_service.set_blockchain(block_entities)
                max_chain_length = len(blocks)
                exchanged_blockchain = True

        return exchanged_blockchain

    def register_node(self, nodes_url: list[str]):
        for node_url in nodes_url:
            parsed_host = urlparse(node_url).hostname  # if not is_local else 'host.docker.internal'
            parsed_port = urlparse(node_url).port
            self._registered_nodes.add(f'{parsed_host}:{parsed_port}')

    def _is_chain_valid(self, blockchain: list[BlockEntity]) -> bool:
        def _is_nonce_valid(block: BlockEntity, nonce: int) -> bool:
            return block.nonce == nonce and block.get_hash()[-2:] == "08"

        for block_idx in range(1, len(blockchain)):
            if blockchain[block_idx - 1].get_hash() != blockchain[block_idx].previous_block_hash:
                return False

            if not _is_nonce_valid(blockchain[block_idx], blockchain[block_idx].nonce):
                return False

        return True
