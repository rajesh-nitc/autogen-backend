import logging
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain_postgres import PGVector
from sqlalchemy.ext.asyncio import AsyncEngine

logger = logging.getLogger(__name__)


class PGVectorService:
    """Service to manage PGVector operations."""

    def __init__(
        self,
        embeddings: AzureOpenAIEmbeddings,
        engine: AsyncEngine,
        collection_name: str,
    ) -> None:
        """Initialize the service."""
        self.vector_store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=engine,
            use_jsonb=True,
        )

    async def similarity_search(self, query: str, k: int = 5):  # noqa: ANN201
        """Run a similarity search on the vector store."""
        return await self.vector_store.asimilarity_search(query, k=k)

    async def add_documents(self, documents: list[Document]) -> None:
        """Add documents to the vector store."""
        try:
            await self.vector_store.aadd_documents(documents)  # Add documents
            # await self.db_session.commit()  # Commit changes
        except Exception:
            # await self.db_session.rollback()  # Rollback on error
            logger.exception("Error adding documents")
            raise

    async def process_and_add_pdfs(
        self, data_folder: str, chunk_size: int = 1000, chunk_overlap: int = 0
    ) -> None:
        """Load and process PDFs, and add them to the vector store."""
        if not os.path.exists(data_folder):
            logger.exception(f"Data folder '{data_folder}' does not exist.")
            return

        pdf_files = self._load_pdf_files(data_folder)
        documents = self._process_pdf_files(pdf_files, chunk_size, chunk_overlap)
        if documents:
            try:
                await self.add_documents(documents)
                logger.info(f"Added {len(documents)} documents to the vector store.")
            except Exception:
                logger.exception("Failed to add documents")
        else:
            logger.info("No documents to add.")

    def _load_pdf_files(self, data_folder: str) -> list[str]:
        """Load all PDF file paths from a given folder."""
        return [
            os.path.join(data_folder, f)
            for f in os.listdir(data_folder)
            if f.endswith(".pdf")
        ]

    def _process_pdf_files(
        self, pdf_files: list[str], chunk_size: int, chunk_overlap: int
    ) -> list[Document]:
        """Process PDF files, splitting them into smaller chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        docs = []
        for pdf_file in pdf_files:
            logger.info(f"Processing {os.path.basename(pdf_file)}...")
            loader = PyPDFLoader(
                pdf_file, extract_images=True, images_inner_format="markdown-img"
            )
            documents = loader.load_and_split(text_splitter)
            docs.extend(documents)
        return docs
