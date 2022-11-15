from fastapi import APIRouter

from .transactions import router as tr_router
from .blocks import router as bl_router
from .mining import router as mine_router
from .wallets import router as wallets_router
from .nodes import router as nodes_router


router = APIRouter()

router.include_router(tr_router)
router.include_router(bl_router)
router.include_router(mine_router)
router.include_router(wallets_router)
router.include_router(nodes_router)
