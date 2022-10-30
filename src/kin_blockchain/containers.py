from dependency_injector import containers, providers

from kin_blockchain.api.mining_service import MiningService
from kin_blockchain.domain.blockchain import Blockchain
from kin_blockchain.domain.services import BlockService, TransactionService
from kin_blockchain.domain.services.wallet_service import WalletService
from kin_blockchain.domain.utils import mine_genesis_block
from kin_blockchain.infrastructure.repositories import IWalletRepository, MemoryWalletRepository


class Repositories(containers.DeclarativeContainer):
    wallet_repository: providers.Singleton[IWalletRepository] = providers.Singleton(
        MemoryWalletRepository
    )


class Services(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    block_service: providers.Singleton[BlockService] = providers.Singleton(
        BlockService,
        genesis_block=mine_genesis_block(),
    )
    transaction_service: providers.Singleton[TransactionService] = providers.Singleton(
        TransactionService
    )
    wallet_service: providers.Singleton[WalletService] = providers.Singleton(
        WalletService,
        wallet_repository=repositories.wallet_repository,
    )


class Container(containers.DeclarativeContainer):
    repositories: providers.Container[Repositories] = providers.Container(
        Repositories
    )

    services: providers.Container[Services] = providers.Container(
        Services,
        repositories=repositories,
    )

    blockchain: providers.Singleton[Blockchain] = providers.Singleton(
        Blockchain,
        block_service=services.block_service,
        transaction_service=services.transaction_service,
        wallet_service=services.wallet_service,
    )

    mining_service: providers.Singleton[MiningService] = providers.Singleton(
        MiningService,
        blockchain=blockchain,
    )
