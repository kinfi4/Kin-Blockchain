from dependency_injector import containers, providers

from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.domain.services import BlockService, TransactionService, MiningService
from kin_blockchain.domain.utils import mine_genesis_block


class Services(containers.DeclarativeContainer):
    block_service: providers.Singleton[BlockService] = providers.Singleton(
        BlockService,
        genesis_block=mine_genesis_block(),
    )
    transaction_service: providers.Singleton[TransactionService ]= providers.Singleton(
        TransactionService
    )


class Container(containers.DeclarativeContainer):
    services: providers.Container[Services] = providers.Container(
        Services
    )

    blockchain: providers.Singleton[Blockchain] = providers.Singleton(
        Blockchain,
        block_service=services.block_service,
        transaction_service=services.transaction_service,
    )

    mining_service: providers.Singleton[MiningService] = providers.Singleton(
        MiningService,
        blockchain=blockchain,
    )
