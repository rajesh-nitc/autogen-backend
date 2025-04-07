import logging
from typing import TYPE_CHECKING, Annotated

from langchain_core.documents import Document

from src.core.connection import db_manager
from src.services.vector_search_service import PGVectorService
from src.utils.model_client import get_azure_openai_embeddings_model_client

if TYPE_CHECKING:
    from langchain_core.documents import Document

logger = logging.getLogger(__name__)


async def get_vector_search_tool(
    query: Annotated[
        str,
        "Search Query.",
    ],
) -> Annotated[
    list[dict],
    "Returns a list of documents with content and metadata (source, page_label)",
]:
    """Perform a vector search on the company policies, health plans and benefits."""
    embeddings = get_azure_openai_embeddings_model_client()

    vector_search_service = PGVectorService(
        embeddings=embeddings,
        engine=db_manager.engine,
        collection_name="company_policies",
    )

    results: list[Document] = await vector_search_service.similarity_search(query, k=5)

    if not results:
        return []
    output = []
    for doc in results:
        metadata = doc.metadata or {}
        output.append(
            {
                "page_content": doc.page_content,
                "source": metadata.get("source", "unknown"),
                "page_label": metadata.get("page_label", "unknown"),
            }
        )
    logger.info(f"Vector search output:========================= {output}")
    return output
