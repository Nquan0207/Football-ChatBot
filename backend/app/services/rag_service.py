import os
import asyncio
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader, DirectoryLoader
from app.core.config import settings
import logging

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
            if os.path.exists(self.vector_db_path):
                self.vector_db = Chroma(
                    persist_directory=self.vector_db_path,
                    embedding_function=self.embeddings
                )
                logger.info("Loaded existing vector database")
            else:
                self.vector_db = Chroma(
                    persist_directory=self.vector_db_path,
                    embedding_function=self.embeddings
                )
                logger.info("Created new vector database")
        except Exception as e:
            logger.error(f"Error initializing vector database: {e}")
            raise
    
    async def add_documents(self, file_paths: List[str]) -> bool:
        """Add documents to the vector database"""
        try:
            documents = []
            
            for file_path in file_paths:
                if os.path.isfile(file_path):
                    loader = TextLoader(file_path)
                    documents.extend(loader.load())
                elif os.path.isdir(file_path):
                    loader = DirectoryLoader(file_path, glob="**/*.txt")
                    documents.extend(loader.load())
            
            if not documents:
                logger.warning("No documents found to add")
                return False
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add to vector database
            self.vector_db.add_documents(chunks)
            self.vector_db.persist()
            
            logger.info(f"Added {len(chunks)} chunks to vector database")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    async def search_similar(self, query: str, k: int = 5) -> List[str]:
        """Search for similar documents"""
        try:
            if not self.vector_db:
                logger.warning("Vector database not initialized")
                return []
            
            results = self.vector_db.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
            
        except Exception as e:
            logger.error(f"Error searching similar documents: {e}")
            return []
    
    async def get_context_for_query(self, query: str, k: int = 3) -> List[str]:
        """Get relevant context for a query"""
        try:
            similar_docs = await self.search_similar(query, k=k)
            return similar_docs
            
        except Exception as e:
            logger.error(f"Error getting context: {e}")
            return []
    
    def get_database_stats(self) -> dict:
        """Get vector database statistics"""
        try:
            if not self.vector_db:
                return {"total_documents": 0, "status": "not_initialized"}
            
            collection = self.vector_db._collection
            count = collection.count()
            
            return {
                "total_documents": count,
                "status": "active",
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
            }
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {"total_documents": 0, "status": "error"} 