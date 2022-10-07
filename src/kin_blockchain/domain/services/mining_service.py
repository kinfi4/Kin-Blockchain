from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.domain.entities import BlockEntity


class MiningService:
    def __init__(self, blockchain: Blockchain):
        self._blockchain = blockchain

    def mine_new_block(self) -> BlockEntity:
        possible_nonce = 0
        while True:
            is_mined, block = self._blockchain.validate_proof(possible_nonce)

            if is_mined:
                return block

            possible_nonce += 1
