from fastapi import APIRouter, Depends, status, Response
from dependency_injector.wiring import inject, Provide

from kin_blockchain.api.models import TransactionModel
from kin_blockchain.domain.services import TransactionService, WalletService
from kin_blockchain.containers import Container


router = APIRouter(prefix='/transactions')


@router.post('', response_model=TransactionModel, status_code=status.HTTP_201_CREATED)
@inject
def create_transaction(
    transaction: TransactionModel,
    transaction_service: TransactionService = Depends(Provide[Container.services.transaction_service]),
    wallet_service: WalletService = Depends(Provide[Container.services.wallet_service]),
):
    if not wallet_service.is_transaction_valid(transaction.sender, transaction.amount):
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content='Sender does not have enough tokens!')

    added_transaction = transaction_service.add_transaction(transaction.to_domain())

    return TransactionModel.from_domain(added_transaction)
