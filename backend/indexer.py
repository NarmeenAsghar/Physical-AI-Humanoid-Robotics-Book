import os
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# ---------------------------
# LOAD ENV VARIABLES
# ---------------------------
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "book_chunks")

# ---------------------------
# CONFIG
# ---------------------------
DOCS_PATH = Path("../website/docs")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ---------------------------
# INIT MODELS
# ---------------------------
print("🔹 Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("🔹 Connecting to Qdrant...")
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# ---------------------------
# CREATE COLLECTION (IF NOT EXISTS)
# ---------------------------
collections = [c.name for c in client.get_collections().collections]

if QDRANT_COLLECTION not in collections:
    print("🔹 Creating Qdrant collection...")
    client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )
else:
    print("✅ Qdrant collection already exists")

# ---------------------------
# UTILS
# ---------------------------
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

# ---------------------------
# READ & INDEX DOCS
# ---------------------------
points = []
point_id = 1
file_count = 0

print("🔹 Reading documentation files...")

for md_file in DOCS_PATH.rglob("*.md"):
    file_count += 1
    text = md_file.read_text(encoding="utf-8")

    chunks = chunk_text(text)

    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "source": str(md_file),
                    "chunk": idx,
                    "text": chunk,
                },
            )
        )
        point_id += 1

# ---------------------------
# INSERT INTO QDRANT
# ---------------------------
print(f"🔹 Total files read: {file_count}")
print(f"🔹 Total chunks created: {len(points)}")
print("🔹 Uploading to Qdrant...")

client.upsert(
    collection_name=QDRANT_COLLECTION,
    points=points,
)

print("✅ Indexing completed successfully!")
