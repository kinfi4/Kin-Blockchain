from fastapi import FastAPI

from kin_blockchain.api import endpoints
from kin_blockchain.containers import Container


def create_container() -> Container:
    container = Container()
    container.init_resources()

    container.wire(packages=[endpoints])

    return container


def create_app(*args, **kwargs) -> FastAPI:
    fastapi_app = FastAPI(
        title='Kinfi4 Blockchain',
    )

    fastapi_app.containers = create_container()
    fastapi_app.include_router(endpoints.tr_router)
    fastapi_app.include_router(endpoints.bl_router)
    fastapi_app.include_router(endpoints.mine_router)

    return fastapi_app
