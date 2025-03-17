import httpx


class HTTPClientSingleton:
    """Singleton class for HTTP client instances."""

    _instances: dict[str, httpx.AsyncClient] = {}

    @staticmethod
    def get_instance(base_url: str, timeout: float = 10.0) -> httpx.AsyncClient:
        """Get an instance of HTTP client for a given base URL.

        :param base_url: str
        :param timeout: float
        :return: httpx.AsyncClient
        """
        if base_url not in HTTPClientSingleton._instances:
            HTTPClientSingleton._instances[base_url] = httpx.AsyncClient(
                base_url=base_url, timeout=timeout
            )
        return HTTPClientSingleton._instances[base_url]

    @staticmethod
    async def close_all_instances() -> None:
        """Close all instances of HTTP clients."""
        for client in HTTPClientSingleton._instances.values():
            await client.aclose()
        HTTPClientSingleton._instances.clear()
