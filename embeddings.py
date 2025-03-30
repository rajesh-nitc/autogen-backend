import asyncio
import logging

from src.core.connection import db_manager
from src.services.vector_search_service import PGVectorService
from src.utils.model_client import get_azure_openai_embeddings_model_client

logger = logging.getLogger(__name__)


async def generate_embeddings() -> None:
    """Generate embeddings for the documents."""
    data_folder = "data"
    embeddings = get_azure_openai_embeddings_model_client()

    vector_search_service = PGVectorService(
        embeddings=embeddings,
        engine=db_manager.engine,
        collection_name="company_policies",
    )

    try:
        await vector_search_service.process_and_add_pdfs(data_folder, chunk_size=1000)
    except Exception:
        logger.exception("Error generating embeddings.")


if __name__ == "__main__":
    asyncio.run(generate_embeddings())
