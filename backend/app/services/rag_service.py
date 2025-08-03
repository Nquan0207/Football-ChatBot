import os
import asyncio
import logging
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma


from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader


from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.vector_db_path = settings.VECTOR_DB_PATH
        self.vector_db = None
        self._initialize_vector_db()
    
    def _initialize_vector_db(self):
        """Initialize or load existing vector database"""
        try:
            self.vector_db = Chroma(
                persist_directory=self.vector_db_path,
                embedding_function=self.embeddings
            )
            logger.info(
                "Loaded existing vector database"
                if os.path.exists(self.vector_db_path)
                else "Created new vector database"
            )
        except Exception as e:
            logger.error(f"Error initializing vector database: {e}")
            raise
    
    async def add_documents(self, file_paths: List[str]) -> bool:
        """Add .txt, .pdf, .docx files to the vector database"""
        try:
            raw_docs = []

            for path in file_paths:
                if os.path.isfile(path):
                    raw_docs.extend(self._load_file(path))
                elif os.path.isdir(path):
                    # walk directory to find supported extensions
                    for root, _, files in os.walk(path):
                        for fname in files:
                            full = os.path.join(root, fname)
                            raw_docs.extend(self._load_file(full))
            
            if not raw_docs:
                logger.warning("No documents found to add")
                return False

            # Split into chunks
            chunks = self.text_splitter.split_documents(raw_docs)

            # Add & persist
            self.vector_db.add_documents(chunks)
            self.vector_db.persist()

            logger.info(f"Added {len(chunks)} chunks to vector database")
            return True

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False

    def _load_file(self, file_path: str):
        """Dispatch loader based on file extension"""
        ext = file_path.lower().split('.')[-1]
        try:
            if ext == "txt":
                loader = TextLoader(file_path)
            elif ext == "pdf":
                loader = PyPDFLoader(file_path)
            elif ext in ("docx", "doc"):
                loader = Docx2txtLoader(file_path)
            else:
                # skip unsupported
                return []
            return loader.load()
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            return []

    async def search_similar(self, query: str, k: int = 5) -> List[str]:
        try:
            results = self.vector_db.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            logger.error(f"Error searching similar documents: {e}")
            return []

    async def get_context_for_query(self, query: str, k: int = 3) -> List[str]:
        return await self.search_similar(query, k)

    def get_database_stats(self) -> dict:
        try:
            if not self.vector_db:
                return {"total_documents": 0, "status": "not_initialized"}
            count = self.vector_db._collection.count()
            return {
                "total_documents": count,
                "status": "active",
                "embedding_model": self.embeddings.model_name
            }
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {"total_documents": 0, "status": "error"}
