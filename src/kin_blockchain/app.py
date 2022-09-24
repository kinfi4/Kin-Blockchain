from fastapi import FastAPI

from kin_blockchain import api
from kin_blockchain.containers import Container


def create_container() -> Container:
    container = Container()
    container.init_resources()

    container.wire(packages=[api])

    return container


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title='Kinfi4 Blockchain',
    )

    fastapi_app.containers = create_container()

    return fastapi_app
