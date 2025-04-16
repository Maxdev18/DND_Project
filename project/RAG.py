"""
RAG (Retrieval-Augmented Generation) Demo Script
Using ChromaDB for vector storage, chunking, and Ollama for both embeddings and LLM generation
"""
import os
import glob
from typing import List, Dict, Any
# Vector database, embedding, and text processing
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
import ollama

class OllamaEmbeddingFunction:
    """Custom embedding function that uses Ollama for embeddings"""
    
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Ollama"""
        embeddings = ollama.embed(model='llama3.2', input=input)

        return embeddings.embeddings

def load_documents(data_dir: str) -> Dict[str, str]:
    """
    Load text documents from a directory
    """
    documents = {}
    for file_path in glob.glob(os.path.join(data_dir, "*.txt")):
        with open(file_path, 'r') as file:
            content = file.read()
            documents[os.path.basename(file_path)] = content
    
    return documents

def chunk_documents(documents: Dict[str, str], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Split documents into smaller chunks for embedding,
    using LangChain's RecursiveCharacterTextSplitter
    """
    chunked_documents = []
    
    # Create the chunker with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    for doc_name, content in documents.items():
        # Apply the chunker to the document text
        chunks = text_splitter.split_text(content)
        
        for i, chunk in enumerate(chunks):
            chunked_documents.append({
                "id": f"{doc_name}_chunk_{i}",
                "text": chunk,
                "metadata": {"source": doc_name, "chunk": i}
          })
    
    return chunked_documents

def setup_chroma_db(chunks: List[Dict[str, Any]], collection_name: str = "dnd_knowledge", use_ollama_embeddings: bool = True, ollama_model: str = "nomic-embed-text") -> chromadb.Collection:
    """
    Set up ChromaDB with document chunks
    """
    # Initialize ChromaDB Ephemeral client
    client = chromadb.Client()
    embedding_function = OllamaEmbeddingFunction(model_name=ollama_model)
    
    # Create or get collection
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    
    # Add documents to collection
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks]
    )
    
    return collection

def retrieve_context(collection: chromadb.Collection, query: str, n_results: int = 3) -> List[str]:
    """
    Retrieve relevant context from ChromaDB based on the query
    """
    return collection.query(
        query_texts=query,
        n_results=n_results,
        include=["documents"]
    )["documents"][0]