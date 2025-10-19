from fastapi import APIRouter

router = APIRouter()

@router.get("/live")
async def live():
    """Liveness probe: process is up."""
    return {"status": "live"}

@router.get("/ready")
async def ready():
    """Readiness probe: dependencies healthy.
    (Stubbed now; will check DB later.)
    """
    return {"status": "ready"}
