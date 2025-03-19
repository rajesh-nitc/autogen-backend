from fastapi import APIRouter

from src.schemas.health import HealthResponse

router: APIRouter = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok")
