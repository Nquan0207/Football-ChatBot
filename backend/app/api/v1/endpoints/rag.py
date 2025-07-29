from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List
from app.services.chat_service import ChatService
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()


def get_chat_service() -> ChatService:
    return ChatService()


@router.post("/documents")
async def add_documents(
    files: List[UploadFile] = File(...),
    chat_service: ChatService = Depends(get_chat_service)
):
    """Add documents to the RAG system"""
    try:
        file_paths = []
        for file in files:
            # Save uploaded file temporarily
            file_path = f"/tmp/{file.filename}"
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            file_paths.append(file_path)
        
        success = await chat_service.add_documents_to_rag(file_paths)
        
        # Clean up temporary files
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if success:
            return {"message": f"Successfully added {len(files)} documents to RAG system"}
        else:
            raise HTTPException(status_code=500, detail="Failed to add documents")
            
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to add documents")


@router.get("/stats")
async def get_rag_stats(
    chat_service: ChatService = Depends(get_chat_service)
):
    """Get RAG system statistics"""
    try:
        stats = chat_service.get_rag_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting RAG stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get RAG statistics")


@router.post("/search")
async def search_documents(
    query: str,
    k: int = 5,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Search for similar documents"""
    try:
        results = await chat_service.rag_service.search_similar(query, k=k)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to search documents") 