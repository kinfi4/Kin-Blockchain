from fastapi import APIRouter

from .transactions import router as tr_router
from .blocks import router as bl_router
from .mining import router as mine_router


router = APIRouter()

router.include_router(tr_router)
router.include_router(bl_router)
router.include_router(mine_router)
