from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from langchain_openai import AzureOpenAIEmbeddings
from langchain_postgres import PGVector
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings


def get_azure_openai_chat_completion_model_client() -> AzureOpenAIChatCompletionClient:
    """Get an Azure OpenAI chat completion model client.

    :return: AzureOpenAIChatCompletionClient
    """
    return AzureOpenAIChatCompletionClient(
        model=settings.AZURE_OPENAI.LLM_MODEL,
        api_key=settings.AZURE_OPENAI.API_KEY.get_secret_value(),
        azure_endpoint=settings.AZURE_OPENAI.ENDPOINT,
        api_version=settings.AZURE_OPENAI.API_VERSION,
    )


def get_azure_openai_embeddings_model_client() -> AzureOpenAIEmbeddings:
    """Get an Azure OpenAI embeddings model client."""
    return AzureOpenAIEmbeddings(
        model=settings.AZURE_OPENAI.EMBEDDING_MODEL,
        api_key=settings.AZURE_OPENAI.API_KEY.get_secret_value(),
        azure_endpoint=settings.AZURE_OPENAI.ENDPOINT,
        api_version=settings.AZURE_OPENAI.API_VERSION,
    )


def get_pgvector_client(
    embeddings: AzureOpenAIEmbeddings, collection_name: str, db_session: AsyncSession
) -> PGVector:
    """Initialize the PGVector vector store."""
    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=db_session,
        use_jsonb=True,
    )
