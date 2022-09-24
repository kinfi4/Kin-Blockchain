from dependency_injector import containers, providers

from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.domain.services import BlockService, TransactionService, MiningService


class Services(containers.Container):
    block_service: BlockService = providers.Singleton(
        BlockService
    )
    transaction_service: TransactionService = providers.Singleton(
        TransactionService
    )


class Container(containers.Container):
    services = providers.DependenciesContainer()

    blockchain: Blockchain = providers.Singleton(
        Blockchain,
        block_service=services.block_service,
        transaction_service=services.transaction_service,
    )

    mining_service: MiningService = providers.Singleton(
        MiningService,
        blockchain=blockchain,
    )
