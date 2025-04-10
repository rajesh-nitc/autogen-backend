import asyncio
import logging

from src.core.connection import db_manager
from src.services.vector_store_service import PGVectorStoreService
from src.utils.model_client import get_azure_openai_embeddings_model_client

logger = logging.getLogger(__name__)


async def create_embeddings() -> None:
    """Create embeddings for the benefits documents."""
    data_folder = "data"
    embeddings = get_azure_openai_embeddings_model_client()

    vector_store_service = PGVectorStoreService(
        embeddings=embeddings,
        engine=db_manager.engine,
        collection_name="benefits",
    )

    try:
        await vector_store_service.process_and_add_pdfs(data_folder, chunk_size=1000)
    except Exception:
        logger.exception("Error creating embeddings.")


if __name__ == "__main__":
    asyncio.run(create_embeddings())
