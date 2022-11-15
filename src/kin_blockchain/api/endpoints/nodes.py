from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from starlette import status

from kin_blockchain.containers import Container
from kin_blockchain.domain.blockchain import Blockchain

router = APIRouter(prefix='/nodes')


@router.post('/')
@inject
async def register_node(
    data: Request,
    blockchain: Blockchain = Depends(Provide[Container.blockchain]),
):
    json_data = await data.json()
    blockchain.register_node(json_data['nodes_url'])

    return JSONResponse(status_code=status.HTTP_200_OK, content=f'All nodes were registered successfully!')


@router.get('/resolve-conflicts')
@inject
def register_node(
    blockchain: Blockchain = Depends(Provide[Container.blockchain]),
):
    blockchain_is_replaced = blockchain.resolve_conflicts()

    message = 'Our blockchain is authoritative!' if not blockchain_is_replaced else 'Our blockchain was replaced!'

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=message,
    )
