import logging
from typing import TYPE_CHECKING, Annotated

from langchain_core.documents import Document

from src.core.connection import db_manager
from src.services.vector_store_service import PGVectorStoreService
from src.utils.model_client import get_azure_openai_embeddings_model_client

if TYPE_CHECKING:
    from langchain_core.documents import Document

logger = logging.getLogger(__name__)


async def search_benefits_tool(
    query: Annotated[
        str,
        "Search Query.",
    ],
) -> Annotated[
    list[dict],
    "Returns a list of documents with content and metadata (source, page_label)",
]:
    """Tool function for performing vector similarity search on internal documents.

    Such documents include employee benefits, including health plans and policies.
    """
    embeddings = get_azure_openai_embeddings_model_client()

    vector_store_service = PGVectorStoreService(
        embeddings=embeddings,
        engine=db_manager.engine,
        collection_name="benefits",
    )

    results: list[Document] = await vector_store_service.similarity_search(query, k=5)

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
    logger.info(f"Benefits documents: ========================= {output}")
    return output
