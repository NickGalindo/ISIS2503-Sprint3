from fastapi import APIRouter
from . import all

router = APIRouter()

router.include_router(all.router)
