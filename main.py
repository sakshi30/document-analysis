from http.client import HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import uuid
from TextProcessor import TextProcessor
from RagSystem import RagSystem
from datetime import datetime

app = FastAPI(title="RAG Document Q&A System", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
text_processor = TextProcessor()
rag_system = RagSystem()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class QueryResponse(BaseModel):
    answer: str
    query_time: float

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
    }

@app.post("/upload")
async def upload_documents(file: UploadFile = File(...)):
    """Uploads and process documents"""
    content = await file.read()
    response = text_processor.decode_content(content)
    if not response or len(response.strip()) < 10:
        raise HTTPException(400, "File appears to be empty or contains no readable text")

    doc_id = str(uuid.uuid4())
    chunks = text_processor.chunk_text(response)
    if not chunks:
        raise HTTPException(400, "Could not extract meaningful text chunks from the document")
    doc_chunks = []
    for i, chunk in enumerate(chunks):
        chunk = {
            'id': f"{doc_id}_{i}",
            'text': chunk,
            'source': file.filename,
            'doc_id': doc_id
        }
        doc_chunks.append(chunk)

    encoding = "utf-8"
    try:
        await rag_system.add_document_chunks(doc_chunks, doc_id, file, encoding)
    except Exception as e:
        print(f"Error adding to ChromaDB: {e}")
        raise HTTPException(500, f"Failed to store document chunks: {str(e)}")

    return {
        'id': doc_id,
        'name': file.filename,
        'size': len(content),
        'chunk_count': len(chunks),
        'message': 'Document uploaded and processed successfully'
    }

@app.post("/query")
async def query_document(request: QueryRequest):
    start_time = datetime.now()
    try:
        # Retrieve relevant chunks
        relevant_chunks = rag_system.search_chunks(request.query, request.top_k)
        context = "\n\n".join([chunk["text"] for chunk in relevant_chunks])
        # Generate answer
        answer = rag_system.generate_answer(request.query, context)

        query_time = (datetime.now() - start_time).total_seconds()

        return QueryResponse(
            answer=answer,
            query_time=query_time
        )

    except Exception as e:
        raise HTTPException(500,f"Error processing query: {str(e)}")


if __name__ == "__main__":
    print("🚀 Starting RAG Document Q&A System")
    print("📚 Features:")
    print("  - Document upload and processing")
    print("  - Intelligent text chunking")
    print("  - TF-IDF based retrieval")
    print("  - Extractive answer generation")
    print("  - RESTful API with FastAPI")
    print("\n🌐 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)