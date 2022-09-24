from pydantic import BaseModel

from kin_blockchain.domain.entities import TransactionEntity


class TransactionModel(BaseModel):
    sender: str
    receiver: str
    amount: float

    def to_domain(self) -> TransactionEntity:
        return TransactionEntity(
            sender=self.sender,
            receiver=self.receiver,
            amount=self.amount,
        )
