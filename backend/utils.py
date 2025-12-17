"""
Utility Functions for RAG Chatbot - Cloud Connected
========================================================
"""

import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

# .env file loading
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Cloud connection settings
# Note: Hardcoded as a fallback to ensure it works, but will try env first
QDRANT_URL = os.getenv("QDRANT_URL", "https://6208a944-b6cd-4e96-b2d4-40e619f896db.europe-west3-0.gcp.cloud.qdrant.io:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.knVAUbUV-odBQxgqjaEqFaxdLy47uYy5vX3WnfSQOXc")

# Embedding model configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
DEFAULT_COLLECTION = "book_chunks"

_qdrant_client = None
_embedding_model = None

# =============================================================================
# QDRANT CLIENT FUNCTIONS
# =============================================================================

def get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        # Always try to connect to Qdrant Cloud
        print(f"[Qdrant] Attempting to connect to: {QDRANT_URL}")
        print(f"[Qdrant] API Key present: {bool(QDRANT_API_KEY)}")

        try:
            client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY,
                timeout=30,  # 30 second timeout
            )
            # Test the connection by listing collections
            collections = client.get_collections()
            collection_names = [c.name for c in collections.collections]
            print(f"[Qdrant] Connected to CLOUD successfully!")
            print(f"[Qdrant] Available collections: {collection_names}")
            _qdrant_client = client
        except Exception as e:
            print(f"[Qdrant] Cloud Connection Failed: {e}")
            print(f"[Qdrant] ERROR: Cannot connect to Qdrant Cloud. Retrieval will not work!")
            # DO NOT fallback to local - raise the error so we know there's a problem
            # Create a local client anyway to prevent crashes, but log the warning
            QDRANT_LOCAL_PATH = "./qdrant_local"
            os.makedirs(QDRANT_LOCAL_PATH, exist_ok=True)
            _qdrant_client = QdrantClient(path=QDRANT_LOCAL_PATH)
            print(f"[Qdrant] WARNING: Using empty LOCAL database as fallback!")

    return _qdrant_client

# =============================================================================
# EMBEDDING FUNCTIONS
# =============================================================================

def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedding_model

def embed_text(text: str) -> List[float]:
    model = get_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()

def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return [emb.tolist() for emb in embeddings]

# =============================================================================
# RETRIEVAL FUNCTIONS (The Core Fix)
# =============================================================================

def retrieve_from_qdrant(
    query: str,
    top_k: int = 5,
    score_threshold: float = 0.2,  # <--- FIXED: Lowered from 0.5 to 0.2
    collection_name: str = DEFAULT_COLLECTION,
    filter_conditions: Optional[Dict] = None
) -> List[Dict[str, Any]]:
    client = get_qdrant_client()

    # Check if collection exists
    try:
        existing = [c.name for c in client.get_collections().collections]
        if collection_name not in existing:
            print(f"[Qdrant] Collection not found: {collection_name}")
            return []
    except:
        pass

    # Generate query embedding
    query_vector = embed_text(query)

    # Perform search using the query_points API
    try:
        # First, check collection has points
        try:
            collection_info = client.get_collection(collection_name)
            print(f"[SEARCH] Collection '{collection_name}' has {collection_info.points_count} points")
        except Exception as info_err:
            print(f"[SEARCH] Could not get collection info: {info_err}")

        # Try search without score_threshold first to see if we get ANY results
        results = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,  # Explicitly request payload
        )

        print(f"[SEARCH] Raw results count: {len(results.points) if results.points else 0}")

        # Debug: print first result's structure
        if results.points and len(results.points) > 0:
            first_hit = results.points[0]
            print(f"[SEARCH] First hit score: {first_hit.score}, payload keys: {list(first_hit.payload.keys()) if first_hit.payload else 'None'}")

        formatted = []
        for hit in results.points:
            # Skip results below score threshold
            if hit.score < score_threshold:
                print(f"[SEARCH] Skipping result with low score: {hit.score}")
                continue

            # Handle both 'text' (from indexer.py) and 'content' (from populate_qdrant.py) field names
            content = hit.payload.get("text", hit.payload.get("content", "")) if hit.payload else ""

            # Skip if no content found
            if not content:
                print(f"[SEARCH] Warning: No content in payload. Keys: {list(hit.payload.keys()) if hit.payload else 'None'}")
                continue

            # Extract chapter/section from payload or derive from source path
            chapter = hit.payload.get("chapter", "Unknown") if hit.payload else "Unknown"
            section = hit.payload.get("section", "Unknown") if hit.payload else "Unknown"

            # If chapter is unknown, try to extract from source file path
            if chapter == "Unknown" and hit.payload and "source" in hit.payload:
                source_path = hit.payload.get("source", "")
                # Extract meaningful info from path like "../website/docs/module-1/intro.md"
                parts = source_path.replace("\\", "/").split("/")
                if len(parts) >= 2:
                    chapter = parts[-2].replace("-", " ").title() if parts[-2] != "docs" else "General"
                    section = parts[-1].replace(".md", "").replace("-", " ").title()

            formatted.append({
                "id": hit.id,
                "score": hit.score,
                "content": content,
                "chapter": chapter,
                "section": section,
                "metadata": {k: v for k, v in hit.payload.items() if k not in ["content", "text"]} if hit.payload else {}
            })

        print(f"[SEARCH] Found {len(formatted)} results for: '{query}'")
        return formatted
    except Exception as e:
        print(f"[SEARCH] Error during retrieval: {e}")
        return []

# =============================================================================
# COLLECTION MANAGEMENT FUNCTIONS
# =============================================================================

def init_qdrant_collection(collection_name: str = DEFAULT_COLLECTION, recreate: bool = False) -> bool:
    """
    Initialize a Qdrant collection if it doesn't exist.

    Args:
        collection_name: Name of the collection to create
        recreate: If True, delete and recreate the collection

    Returns:
        bool: True if collection exists/created successfully
    """
    client = get_qdrant_client()

    try:
        existing = [c.name for c in client.get_collections().collections]

        if recreate and collection_name in existing:
            print(f"[Qdrant] Deleting existing collection: {collection_name}")
            client.delete_collection(collection_name)
            existing.remove(collection_name)

        if collection_name not in existing:
            print(f"[Qdrant] Creating collection: {collection_name}")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )
            print(f"[Qdrant] Collection '{collection_name}' created successfully")
        else:
            print(f"[Qdrant] Collection '{collection_name}' already exists")

        return True
    except Exception as e:
        print(f"[Qdrant] Error initializing collection: {e}")
        return False


def get_collection_info(collection_name: str = DEFAULT_COLLECTION) -> Optional[Dict[str, Any]]:
    """
    Get information about a Qdrant collection.

    Args:
        collection_name: Name of the collection

    Returns:
        Dict with collection info or None if not found
    """
    client = get_qdrant_client()

    try:
        info = client.get_collection(collection_name)
        return {
            "name": collection_name,
            "points_count": info.points_count,
            "vector_size": info.config.params.vectors.size,
            "distance": str(info.config.params.vectors.distance),
            "status": str(info.status),
        }
    except Exception as e:
        print(f"[Qdrant] Error getting collection info: {e}")
        return None


def upsert_chunks(chunks: List[Dict[str, Any]], collection_name: str = DEFAULT_COLLECTION) -> int:
    """
    Insert or update chunks in the Qdrant collection.

    Args:
        chunks: List of chunk dicts with 'id', 'content', and optional 'metadata'
        collection_name: Target collection name

    Returns:
        int: Number of chunks upserted
    """
    client = get_qdrant_client()

    points = []
    for chunk in chunks:
        # Generate embedding for the content
        content = chunk.get("content", "")
        embedding = embed_text(content)

        # Build payload
        payload = {
            "content": content,
            "chapter": chunk.get("metadata", {}).get("chapter", "Unknown"),
            "section": chunk.get("metadata", {}).get("section", "Unknown"),
        }
        # Add any additional metadata
        if "metadata" in chunk:
            for k, v in chunk["metadata"].items():
                if k not in payload:
                    payload[k] = v

        points.append(PointStruct(
            id=chunk.get("id", hash(content) % (10**9)),
            vector=embedding,
            payload=payload,
        ))

    if points:
        client.upsert(collection_name=collection_name, points=points)
        print(f"[Qdrant] Upserted {len(points)} chunks to '{collection_name}'")

    return len(points)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50, metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(text):
        end = start + chunk_size
        chunk_content = text[start:end].strip()
        chunks.append({
            "id": chunk_id,
            "content": chunk_content,
            "metadata": {"chunk_index": chunk_id, **(metadata or {})}
        })
        chunk_id += 1
        start = end - overlap
    return chunks

def health_check() -> Dict[str, Any]:
    try:
        client = get_qdrant_client()
        collections = [c.name for c in client.get_collections().collections]
        return {"qdrant": "healthy", "collections": collections}
    except Exception as e:
        return {"qdrant": f"error: {str(e)}"}