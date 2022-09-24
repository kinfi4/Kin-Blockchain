from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from kin_blockchain.containers import Container
from kin_blockchain.api.models import BlockModel
from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.domain.entities import TransactionEntity
from kin_blockchain.domain.services import MiningService, TransactionService

router = APIRouter(prefix='/mine')


@router.get('', response_model=BlockModel)
@inject
def mine_block(
    miner_address: str,
    mining_service: MiningService = Depends(Provide[Container.mining_service]),
    blockchain: Blockchain = Depends(Provide[Container.blockchain]),
    transaction_service: TransactionService = Depends(Provide[Container.services.transaction_service])
):
    nonce = mining_service.mine_new_block()

    transaction_reward = TransactionEntity(
        sender='0',
        receiver=miner_address,
        amount=1
    )
    transaction_service.add_transaction(transaction_reward)

    new_block = blockchain.create_block(nonce)

    return BlockModel.from_domain(new_block)
