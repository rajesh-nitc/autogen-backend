import httpx

from src.core.settings import settings


class HTTPClientSingleton:
    _instance = None

    @staticmethod
    def get_instance() -> httpx.AsyncClient:
        if HTTPClientSingleton._instance is None:
            HTTPClientSingleton._instance = httpx.AsyncClient(
                base_url=settings.HTTP_CLIENT_BASE_URL, timeout=10.0
            )
        return HTTPClientSingleton._instance

    @staticmethod
    async def close_instance():
        if HTTPClientSingleton._instance:
            await HTTPClientSingleton._instance.aclose()  # type: ignore
            HTTPClientSingleton._instance = None
