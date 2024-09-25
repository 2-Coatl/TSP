import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from storage.src.storage_service import StorageService
from storage.src.utils.config import Config
from storage.src.utils.logger import LoggerManager

app = FastAPI()
config = Config()
logger = LoggerManager(__name__)
storage_service = StorageService()

class DocumentCreate(BaseModel):
    filename: str
    file_path: str
    file_size: int
    source_language: str
    target_language: str

@app.on_event("startup")
async def startup_event():
    logger.log_message("Initializing database...", level='info')
    storage_service.initialize_database()
    logger.log_message("Database initialized successfully", level='info')

@app.post("/documents/", response_model=int)
async def create_document(document: DocumentCreate):
    try:
        doc_id = storage_service.add_new_document(
            document.filename,
            document.file_path,
            document.file_size,
            document.source_language,
            document.target_language
        )
        return doc_id
    except Exception as e:
        logger.log_message(f"Error creating document: {str(e)}", level='error')
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/documents/{doc_id}")
async def get_document(doc_id: int):
    document = storage_service.get_document(doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@app.put("/documents/{doc_id}/status")
async def update_document_status(doc_id: int, new_status: str):
    success = storage_service.update_document_status(doc_id, new_status)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Status updated successfully"}

@app.get("/documents/for_translation")
async def get_documents_for_translation(limit: int = 10, offset: int = 0):
    return storage_service.get_documents_for_translation(limit, offset)

if __name__ == "__main__":
    logger.log_message("Starting storage service...", level='info')
    uvicorn.run("storage.src.main:app", host="0.0.0.0", port=8000, reload=True)
    logger.log_message("Storage service stopped", level='info')