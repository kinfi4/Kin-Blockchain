from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from kin_blockchain.api.models import BlockModel
from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.containers import Container

router = APIRouter(prefix='/blocks')


@router.get('/full-blockchain', response_model=list[BlockModel])
@inject
def get_full_blockchain(
    blockchain: Blockchain = Depends(Provide[Container.blockchain]),
):
    blocks = blockchain.get_blockchain()

    return [BlockModel.from_domain(block) for block in blocks]
