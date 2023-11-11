from fastapi import APIRouter, Request

from persistence import updates

router = APIRouter()

@router.post("/runShit")
async def runShit(request: Request, shit: str):
    return updates.run(request.app.state.redundantConnectionPool, request.app.state.baseConnectionPool, shit)
