import chromadb
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests

class RagSystem:
    def __init__(self, collection_name: str = "document_chunks", persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB client and collection"""
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = collection_name
        self.executor = ThreadPoolExecutor(max_workers=2)  # For async operations

        # Get or create collection with optimized settings
        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,  # Use the parameter, not hardcoded string
                metadata={
                    "hnsw:space": "cosine",
                    "hnsw:construction_ef": 100,  # Reduced from 200 for faster indexing
                    "hnsw:M": 8  # Reduced from 16 for lower memory usage
                }
            )
            print(f"ChromaDB collection '{collection_name}' initialized successfully")
        except Exception as e:
            print(f"Error initializing ChromaDB collection: {e}")
            raise

    async def add_document_chunks(self, chunks, doc_id, file, encoding_used):
        """Add document chunks to ChromaDB collection"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.add_chunks,
            chunks, doc_id, file, encoding_used
        )

    def add_chunks(self, chunks, doc_id, file, encoding_used):
        """Add document chunks to ChromaDB collection"""
        if not chunks:
            print("No chunks to add")
            return

        try:
            # Increase batch size for better performance
            batch_size = 100  # Increased from 20
            total_added = 0

            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]

                documents = []
                metadatas = []
                ids = []

                for chunk_data in batch_chunks:
                    # Extract text from chunk object correctly
                    if isinstance(chunk_data, dict):
                        chunk_text = chunk_data.get('text', '')
                        chunk_id = chunk_data.get('id', f"{doc_id}_{len(documents)}")
                    else:
                        # If chunk_data is just a string
                        chunk_text = str(chunk_data)
                        chunk_id = f"{doc_id}_{len(documents)}"

                    if not chunk_text.strip():
                        continue  # Skip empty chunks

                    documents.append(chunk_text)
                    metadatas.append({
                        'source': file.filename,
                        'doc_id': doc_id,
                        'chunk_index': i + len(documents) - 1,
                        'upload_timestamp': datetime.now().isoformat(),
                        'encoding_used': encoding_used,
                        'chunk_length': len(chunk_text)
                    })
                    ids.append(chunk_id)
                if documents:  # Only add if we have documents
                    try:
                        print("Preparing")
                        # Add batch to ChromaDB
                        self.collection.add(
                            documents=documents,
                            metadatas=metadatas,
                            ids=ids
                        )
                        total_added += len(documents)
                        print(f"Added batch: {len(documents)} chunks, Total: {total_added}")
                    except Exception as e:
                        print(f"Error adding batch to ChromaDB: {e}")
                        # Continue with next batch instead of failing completely
                        continue

            print(f"Successfully added {total_added} chunks to ChromaDB for document {doc_id}")
            return total_added

        except Exception as e:
            print(f"Error in add_document_chunks: {e}")
            raise

    def search_chunks(self, query_str: str, top_k: int = 5):
        results = self.collection.query(
            query_texts=[query_str],
            n_results=top_k
        )

        matched_chunks = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            matched_chunks.append({
                "text": doc,
                "source": metadata['source'],
                "chunk_index": metadata['chunk_index']
            })
        return matched_chunks

    def generate_answer(self, query, chunks):
        prompt = f"""
        Use the following context to answer the question as accurately as possible.

        Context:
        {chunks}

        Question:
        {query}

        Answer:"""
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",  # or any model you have
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        answer = response.json()["response"]
        print(answer)
        return answer
