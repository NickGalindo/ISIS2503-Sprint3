from fastapi import APIRouter, Request
from pydantic import BaseModel

from persistence import updates

class Stuff(BaseModel):
    com: str

router = APIRouter()

@router.post("/run")
async def run(request: Request, com: Stuff):
    print(com.com)
    return await updates.run(request.app.state.redundantConnectionPool, request.app.state.baseConnectionPool, com.com)
