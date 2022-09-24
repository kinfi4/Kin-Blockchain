from kin_blockchain.domain.blockchain import Blockchain


class MiningService:
    def __init__(self, blockchain: Blockchain):
        self._blockchain = blockchain

    def mine_new_block(self) -> int:
        possible_nonce = 0
        while not self._blockchain.validate_proof(possible_nonce):
            possible_nonce += 1

        return possible_nonce
