from fastapi import APIRouter, Request
from pydantic import BaseModel

class User(BaseModel):
    username: str
    name: str
    password: str

from persistence import queries

router = APIRouter()

@router.post("/query")
async def query(request: Request, q: str):
    return await queries.query(request.app.state.redundantConnectionPool, request.app.state.baseConnectionPool, q)
