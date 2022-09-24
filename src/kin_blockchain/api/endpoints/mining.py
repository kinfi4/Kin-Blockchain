from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from kin_blockchain.containers import Container
from kin_blockchain.api.models import BlockModel
from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.domain.services import MiningService


router = APIRouter(prefix='mine')


@inject
@router.get('', response_model=BlockModel)
def mine_block(
    mining_service: MiningService = Depends(Provide[Container.mining_service]),
    blockchain: Blockchain = Depends(Provide[Container.blockchain]),
):
    nonce = mining_service.mine_new_block()
    new_block = blockchain.create_block(nonce)

    return BlockModel.from_domain(new_block)
