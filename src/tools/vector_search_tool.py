import logging
from typing import Annotated

from src.core.connection import db_manager
from src.core.dependencies import get_db_session
from src.services.vector_search_service import PGVectorService
from src.utils.model_client import get_azure_openai_embeddings_model_client

logger = logging.getLogger(__name__)


async def get_vector_search_tool(
    query: Annotated[
        str,
        "Query on company policies, health benefits and other company benefits.",
    ],
) -> Annotated[str, "Returns context on company policies and benefits"]:
    """Employees will ask about company policies, health plans and benefits."""
    embeddings = get_azure_openai_embeddings_model_client()

    async with get_db_session() as session:
        vector_service = PGVectorService(
            embeddings=embeddings,
            db_session=session,
            engine=db_manager.engine,
            collection_name="company_policies",
        )

        results = await vector_service.similarity_search(query, k=5)
        if not results:
            return "No relevant context found."

        # Process and format the results
        context = "\n\n".join(
            [
                f"Result {i + 1}:\n{result.page_content}"
                for i, result in enumerate(results)
            ]
        )

        # Log the results
        for i, result in enumerate(results):
            logger.info(f"===== Result {i + 1}: {result.page_content}")

        return context
