import os
import time
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# ---------------------------
# LOAD ENV VARIABLES
# ---------------------------
load_dotenv()

# Hardcoded fallback for cloud connection (same as utils.py)
QDRANT_URL = os.getenv("QDRANT_URL", "https://6208a944-b6cd-4e96-b2d4-40e619f896db.europe-west3-0.gcp.cloud.qdrant.io:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.knVAUbUV-odBQxgqjaEqFaxdLy47uYy5vX3WnfSQOXc")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "book_chunks")

# ---------------------------
# CONFIG
# ---------------------------
DOCS_PATH = Path("../website/docs")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
BATCH_SIZE = 50  # Upload in smaller batches to avoid timeouts

# ---------------------------
# INIT MODELS
# ---------------------------
print("🔹 Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("🔹 Connecting to Qdrant...")
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=60,  # Increase timeout to 60 seconds
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
# INSERT INTO QDRANT (in batches)
# ---------------------------
print(f"🔹 Total files read: {file_count}")
print(f"🔹 Total chunks created: {len(points)}")
print(f"🔹 Uploading to Qdrant in batches of {BATCH_SIZE}...")

total_batches = (len(points) + BATCH_SIZE - 1) // BATCH_SIZE
uploaded = 0

for i in range(0, len(points), BATCH_SIZE):
    batch = points[i:i + BATCH_SIZE]
    batch_num = (i // BATCH_SIZE) + 1

    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            client.upsert(
                collection_name=QDRANT_COLLECTION,
                points=batch,
            )
            uploaded += len(batch)
            print(f"   ✓ Batch {batch_num}/{total_batches} uploaded ({uploaded}/{len(points)} points)")
            break
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"   ⚠ Batch {batch_num} failed, retrying ({retry_count}/{max_retries})...")
                time.sleep(2)  # Wait before retry
            else:
                print(f"   ✗ Batch {batch_num} failed after {max_retries} retries: {e}")
                raise

print(f"✅ Indexing completed! {uploaded} chunks uploaded to Qdrant Cloud.")
