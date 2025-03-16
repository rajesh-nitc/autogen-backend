from fastapi import APIRouter

from src.schemas.health_schema import HealthResponse

router: APIRouter = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    return HealthResponse(status="ok")
