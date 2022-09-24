from dependency_injector import containers, providers

from kin_blockchain.domain.services import BlockService, TransactionService, MiningService


class Services(containers.Container):
    block_service: BlockService = providers.Singleton(
        BlockService
    )
    transaction_service: TransactionService = providers.Singleton(
        TransactionService
    )
    mining_service: MiningService = providers.Singleton(
        MiningService
    )


class Container(containers.Container):
    services = providers.DependenciesContainer()
