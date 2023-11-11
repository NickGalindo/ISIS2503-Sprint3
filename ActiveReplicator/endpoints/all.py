from fastapi import APIRouter, Request
from pydantic import BaseModel

class User(BaseModel):
    username: str
    name: str
    password: str

from persistence import updates

router = APIRouter()

@router.post("/run")
async def run(request: Request, com: str):
    return await updates.run(request.app.state.redundantConnectionPool, request.app.state.baseConnectionPool, com)
