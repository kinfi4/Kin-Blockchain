from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from kin_blockchain.api.models import TransactionModel
from kin_blockchain.domain.services import TransactionService
from kin_blockchain.containers import Container


router = APIRouter(prefix='/transactions')


@inject
@router.post('', response_model=TransactionModel)
def create_transaction(
    transaction: TransactionModel,
    transaction_service: TransactionService = Depends(Provide[Container.services.transaction_service])
):
    added_transaction = transaction_service.add_transaction(transaction.to_domain())

    return JSONResponse(added_transaction.to_dict())
