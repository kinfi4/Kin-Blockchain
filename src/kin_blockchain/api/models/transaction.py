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

    @classmethod
    def from_domain(cls, transaction_entity: TransactionEntity) -> "TransactionModel":
        return cls(
            sender=transaction_entity.sender,
            receiver=transaction_entity.receiver,
            amount=transaction_entity.amount,
        )
