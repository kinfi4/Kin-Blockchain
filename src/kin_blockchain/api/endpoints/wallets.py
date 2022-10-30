from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from kin_blockchain.api.models import WalletModel
from kin_blockchain.domain.services import WalletService
from kin_blockchain.containers import Container


router = APIRouter(prefix='/wallets')


@router.get('', response_model=list[WalletModel])
@inject
def get_wallets(
    user_id: Optional[str] = None,
    wallet_service: WalletService = Depends(Provide[Container.services.wallet_service]),
):
    if user_id:
        user_wallet_entity = wallet_service.get_user_wallet(user_id=user_id)
        return [WalletModel.from_domain(user_wallet_entity)]

    return [WalletModel.from_domain(wallet) for wallet in wallet_service.get_all_wallets()]
