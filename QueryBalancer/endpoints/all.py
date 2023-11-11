from fastapi import APIRouter, Request
from pydantic import BaseModel

from persistence import queries

class Qry(BaseModel):
    q: str

router = APIRouter()

@router.post("/query")
async def query(request: Request, q: Qry):
    return await queries.query(request.app.state.redundantConnectionPool, request.app.state.baseConnectionPool, q.q)
