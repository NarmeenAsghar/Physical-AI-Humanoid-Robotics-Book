"""
Utility Functions for RAG Chatbot - Local Embedded Mode
========================================================
This module provides vector database and embedding utilities
using a LOCAL embedded Qdrant instance (no Docker, no external server).

Features:
- Local Qdrant embedded mode (data stored in ./qdrant_local/)
- Sentence-transformer embeddings (all-MiniLM-L6-v2, 384 dimensions)
- Collection management and retrieval functions

IMPORTANT: No external Qdrant server required - runs entirely in-process.

@author AI Backend Developer
@version 2.0.0 (Local Embedded Mode)
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

# =============================================================================
# CONFIGURATION
# =============================================================================

# Path for local embedded Qdrant storage
# This directory will be created automatically if it doesn't exist
QDRANT_LOCAL_PATH = "./qdrant_local"

# Embedding model configuration
# all-MiniLM-L6-v2 produces 384-dimensional vectors
# It's fast, lightweight, and good for semantic search
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Default collection name for book content
DEFAULT_COLLECTION = "book_chunks"

# =============================================================================
# GLOBAL INSTANCES (Lazy Loaded)
# =============================================================================

_qdrant_client: Optional[QdrantClient] = None
_embedding_model: Optional[SentenceTransformer] = None


# =============================================================================
# QDRANT CLIENT FUNCTIONS
# =============================================================================

def get_qdrant_client() -> QdrantClient:
    """
    Get or create a local embedded Qdrant client.

    This uses Qdrant's embedded mode which stores data locally
    in the ./qdrant_local directory. No Docker or external server needed.

    Returns:
        QdrantClient: A client connected to local embedded storage

    Example:
        >>> client = get_qdrant_client()
        >>> collections = client.get_collections()
    """
    global _qdrant_client

    if _qdrant_client is None:
        # Create the storage directory if it doesn't exist
        os.makedirs(QDRANT_LOCAL_PATH, exist_ok=True)

        # Initialize client in embedded mode (local storage)
        _qdrant_client = QdrantClient(path=QDRANT_LOCAL_PATH)
        print(f"[Qdrant] Initialized local embedded client at: {QDRANT_LOCAL_PATH}")

    return _qdrant_client


def close_qdrant_client():
    """
    Close the Qdrant client connection.

    Call this when shutting down the application to ensure
    all data is properly persisted to disk.
    """
    global _qdrant_client

    if _qdrant_client is not None:
        _qdrant_client.close()
        _qdrant_client = None
        print("[Qdrant] Client closed")


# =============================================================================
# EMBEDDING FUNCTIONS
# =============================================================================

def get_embedding_model() -> SentenceTransformer:
    """
    Get or create the sentence transformer embedding model.

    Uses all-MiniLM-L6-v2 which produces 384-dimensional vectors.
    The model is cached after first load for performance.

    Returns:
        SentenceTransformer: The loaded embedding model
    """
    global _embedding_model

    if _embedding_model is None:
        print(f"[Embeddings] Loading model: {EMBEDDING_MODEL_NAME}")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print(f"[Embeddings] Model loaded successfully")

    return _embedding_model


def embed_text(text: str) -> List[float]:
    """
    Generate embedding vector for a text string.

    Args:
        text: The text to embed

    Returns:
        List[float]: A 384-dimensional embedding vector

    Example:
        >>> vector = embed_text("Hello world")
        >>> len(vector)
        384
    """
    model = get_embedding_model()

    # Generate embedding (returns numpy array)
    embedding = model.encode(text, convert_to_numpy=True)

    # Convert to list for Qdrant compatibility
    return embedding.tolist()


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embedding vectors for multiple texts (batch processing).

    More efficient than calling embed_text() multiple times
    as it processes all texts in a single batch.

    Args:
        texts: List of texts to embed

    Returns:
        List[List[float]]: List of 384-dimensional embedding vectors
    """
    model = get_embedding_model()

    # Batch encode all texts
    embeddings = model.encode(texts, convert_to_numpy=True)

    # Convert to list of lists
    return [emb.tolist() for emb in embeddings]


# =============================================================================
# COLLECTION MANAGEMENT
# =============================================================================

def init_qdrant_collection(
    collection_name: str = DEFAULT_COLLECTION,
    vector_size: int = EMBEDDING_DIMENSION,
    distance: Distance = Distance.COSINE,
    recreate: bool = False
) -> bool:
    """
    Initialize a Qdrant collection if it doesn't exist.

    Args:
        collection_name: Name of the collection to create
        vector_size: Dimension of vectors (default: 384 for MiniLM)
        distance: Distance metric (default: COSINE)
        recreate: If True, delete and recreate existing collection

    Returns:
        bool: True if collection was created, False if it already existed

    Example:
        >>> created = init_qdrant_collection("book_chunks")
        >>> print(f"Collection created: {created}")
    """
    client = get_qdrant_client()

    # Get list of existing collections
    existing = [c.name for c in client.get_collections().collections]

    # Handle recreation
    if recreate and collection_name in existing:
        client.delete_collection(collection_name)
        print(f"[Qdrant] Deleted existing collection: {collection_name}")
        existing.remove(collection_name)

    # Create if doesn't exist
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance
            )
        )
        print(f"[Qdrant] Created collection: {collection_name} (dim={vector_size})")
        return True
    else:
        print(f"[Qdrant] Collection already exists: {collection_name}")
        return False


def delete_collection(collection_name: str = DEFAULT_COLLECTION) -> bool:
    """
    Delete a Qdrant collection.

    Args:
        collection_name: Name of the collection to delete

    Returns:
        bool: True if deleted, False if didn't exist
    """
    client = get_qdrant_client()

    existing = [c.name for c in client.get_collections().collections]

    if collection_name in existing:
        client.delete_collection(collection_name)
        print(f"[Qdrant] Deleted collection: {collection_name}")
        return True
    else:
        print(f"[Qdrant] Collection not found: {collection_name}")
        return False


def get_collection_info(collection_name: str = DEFAULT_COLLECTION) -> Optional[Dict]:
    """
    Get information about a collection.

    Args:
        collection_name: Name of the collection

    Returns:
        Dict with collection info or None if not found
    """
    client = get_qdrant_client()

    try:
        info = client.get_collection(collection_name)
        # Handle different qdrant-client versions
        points_count = getattr(info, 'points_count', None) or getattr(info, 'vectors_count', 0)

        # Get vector config - handle different API versions
        vector_config = info.config.params.vectors
        if hasattr(vector_config, 'size'):
            vector_size = vector_config.size
            distance = vector_config.distance.value if hasattr(vector_config.distance, 'value') else str(vector_config.distance)
        else:
            # Newer API might have different structure
            vector_size = EMBEDDING_DIMENSION
            distance = "Cosine"

        return {
            "name": collection_name,
            "points_count": points_count,
            "status": info.status.value if hasattr(info.status, 'value') else str(info.status),
            "vector_size": vector_size,
            "distance": distance,
        }
    except Exception as e:
        print(f"[Qdrant] Error getting collection info: {e}")
        return None


# =============================================================================
# DATA INSERTION
# =============================================================================

def upsert_chunks(
    chunks: List[Dict[str, Any]],
    collection_name: str = DEFAULT_COLLECTION
) -> int:
    """
    Insert or update text chunks into Qdrant.

    Each chunk should have:
    - id: Unique identifier (int or str)
    - content: The text content
    - metadata: Optional dict with chapter, section, etc.

    Args:
        chunks: List of chunk dictionaries
        collection_name: Target collection name

    Returns:
        int: Number of chunks upserted

    Example:
        >>> chunks = [
        ...     {"id": 1, "content": "Hello world", "metadata": {"chapter": "Intro"}}
        ... ]
        >>> count = upsert_chunks(chunks)
    """
    client = get_qdrant_client()

    # Ensure collection exists
    init_qdrant_collection(collection_name)

    # Extract texts for batch embedding
    texts = [chunk["content"] for chunk in chunks]
    vectors = embed_texts(texts)

    # Build points for upsert
    points = []
    for i, chunk in enumerate(chunks):
        # Prepare payload (metadata + content)
        payload = {
            "content": chunk["content"],
            **(chunk.get("metadata", {}))
        }

        points.append(PointStruct(
            id=chunk["id"] if isinstance(chunk["id"], int) else hash(chunk["id"]) % (10**9),
            vector=vectors[i],
            payload=payload
        ))

    # Upsert in batches of 100
    batch_size = 100
    total_upserted = 0

    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=collection_name,
            points=batch
        )
        total_upserted += len(batch)
        print(f"[Qdrant] Upserted batch: {total_upserted}/{len(points)}")

    return total_upserted


# =============================================================================
# RETRIEVAL FUNCTIONS
# =============================================================================

def retrieve_from_qdrant(
    query: str,
    top_k: int = 5,
    score_threshold: float = 0.5,
    collection_name: str = DEFAULT_COLLECTION,
    filter_conditions: Optional[Dict] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve similar chunks from Qdrant based on a text query.

    Args:
        query: The search query text
        top_k: Maximum number of results to return
        score_threshold: Minimum similarity score (0-1)
        collection_name: Collection to search
        filter_conditions: Optional metadata filters

    Returns:
        List of dicts with content, metadata, and similarity score

    Example:
        >>> results = retrieve_from_qdrant("What is ROS2?", top_k=3)
        >>> for r in results:
        ...     print(f"Score: {r['score']:.2f} - {r['content'][:50]}...")
    """
    client = get_qdrant_client()

    # Check if collection exists
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        print(f"[Qdrant] Collection not found: {collection_name}")
        return []

    # Generate query embedding
    query_vector = embed_text(query)

    # Build filter if provided
    search_filter = None
    if filter_conditions:
        conditions = []
        for key, value in filter_conditions.items():
            conditions.append(
                FieldCondition(key=key, match=MatchValue(value=value))
            )
        search_filter = Filter(must=conditions)

    # Perform search using query_points (qdrant-client >= 1.10)
    # This is the new API that replaced the older search() method
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=search_filter,
        limit=top_k,
        score_threshold=score_threshold
    )

    # Format results - query_points returns a QueryResponse with .points attribute
    formatted = []
    for hit in results.points:
        formatted.append({
            "id": hit.id,
            "score": hit.score,
            "content": hit.payload.get("content", ""),
            "chapter": hit.payload.get("chapter", "Unknown"),
            "section": hit.payload.get("section", "Unknown"),
            "metadata": {k: v for k, v in hit.payload.items() if k != "content"}
        })

    return formatted


def retrieve_by_vector(
    query_vector: List[float],
    top_k: int = 5,
    score_threshold: float = 0.5,
    collection_name: str = DEFAULT_COLLECTION
) -> List[Dict[str, Any]]:
    """
    Retrieve similar chunks using a pre-computed vector.

    Use this when you already have an embedding vector
    (e.g., from a previous computation).

    Args:
        query_vector: Pre-computed embedding vector (384 dimensions)
        top_k: Maximum number of results
        score_threshold: Minimum similarity score
        collection_name: Collection to search

    Returns:
        List of result dicts with content and scores
    """
    client = get_qdrant_client()

    # Check if collection exists
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        print(f"[Qdrant] Collection not found: {collection_name}")
        return []

    # Perform search using query_points (qdrant-client >= 1.10)
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        score_threshold=score_threshold
    )

    # Format results
    return [
        {
            "id": hit.id,
            "score": hit.score,
            "content": hit.payload.get("content", ""),
            "chapter": hit.payload.get("chapter", "Unknown"),
            "section": hit.payload.get("section", "Unknown"),
            "metadata": {k: v for k, v in hit.payload.items() if k != "content"}
        }
        for hit in results.points
    ]


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    metadata: Optional[Dict] = None
) -> List[Dict[str, Any]]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text: The text to chunk
        chunk_size: Target size of each chunk in characters
        overlap: Number of characters to overlap between chunks
        metadata: Optional metadata to attach to all chunks

    Returns:
        List of chunk dicts with id, content, and metadata

    Example:
        >>> chunks = chunk_text(long_text, chunk_size=300, overlap=30)
        >>> print(f"Created {len(chunks)} chunks")
    """
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk_content = text[start:end]

        # Try to break at sentence boundary
        if end < len(text):
            last_period = chunk_content.rfind('.')
            last_newline = chunk_content.rfind('\n')
            break_point = max(last_period, last_newline)

            if break_point > chunk_size // 2:
                end = start + break_point + 1
                chunk_content = text[start:end]

        chunks.append({
            "id": chunk_id,
            "content": chunk_content.strip(),
            "metadata": {
                "chunk_index": chunk_id,
                "start_char": start,
                "end_char": end,
                **(metadata or {})
            }
        })

        chunk_id += 1
        start = end - overlap

    return chunks


# =============================================================================
# HEALTH CHECK
# =============================================================================

def health_check() -> Dict[str, Any]:
    """
    Check the health of Qdrant and embedding services.

    Returns:
        Dict with status information
    """
    status = {
        "qdrant": "unknown",
        "embeddings": "unknown",
        "collections": [],
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_dimension": EMBEDDING_DIMENSION,
        "storage_path": QDRANT_LOCAL_PATH,
    }

    # Check Qdrant
    try:
        client = get_qdrant_client()
        collections = client.get_collections().collections
        status["qdrant"] = "healthy"
        status["collections"] = [c.name for c in collections]
    except Exception as e:
        status["qdrant"] = f"error: {str(e)}"

    # Check embeddings
    try:
        test_vector = embed_text("test")
        if len(test_vector) == EMBEDDING_DIMENSION:
            status["embeddings"] = "healthy"
        else:
            status["embeddings"] = f"error: unexpected dimension {len(test_vector)}"
    except Exception as e:
        status["embeddings"] = f"error: {str(e)}"

    return status


# =============================================================================
# MAIN (for testing)
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("RAG Utils - Local Qdrant Embedded Mode Test")
    print("=" * 60)

    # Health check
    print("\n1. Health Check:")
    health = health_check()
    for key, value in health.items():
        print(f"   {key}: {value}")

    # Test embedding
    print("\n2. Embedding Test:")
    test_text = "What is ROS2 and how does it work?"
    vector = embed_text(test_text)
    print(f"   Text: '{test_text}'")
    print(f"   Vector dimension: {len(vector)}")
    print(f"   First 5 values: {vector[:5]}")

    # Test collection
    print("\n3. Collection Test:")
    init_qdrant_collection("test_collection", recreate=True)
    info = get_collection_info("test_collection")
    print(f"   Collection info: {info}")

    # Cleanup
    delete_collection("test_collection")

    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)
