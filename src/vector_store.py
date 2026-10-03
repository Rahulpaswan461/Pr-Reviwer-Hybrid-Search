import math
import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from pinecone_text.sparse import BM25Encoder

load_dotenv()

EMBEDDING_DIMENSION = 3072
HYBRID_ALPHA = 0.5
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
NAMESPACE = os.getenv("PINECONE_NAMESPACE", "")


def _required_env(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


pinecone = Pinecone(api_key=_required_env("PINECONE_API_KEY"))
if not INDEX_NAME:
    raise ValueError("Missing required environment variable: PINECONE_INDEX_NAME")

if not pinecone.has_index(INDEX_NAME):
    pinecone.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIMENSION,
        metric="dotproduct",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index_description = pinecone.describe_index(INDEX_NAME)
if index_description.metric != "dotproduct":
    raise ValueError(
        f"Pinecone index {INDEX_NAME!r} uses metric "
        f"{index_description.metric!r}; hybrid search with sparse vectors "
        "requires a dotproduct index. Create a new dotproduct index, set "
        "PINECONE_INDEX_NAME to its name, and re-index the repository. "
        "The existing index cannot be changed in place."
    )
if index_description.dimension != EMBEDDING_DIMENSION:
    raise ValueError(
        f"Pinecone index {INDEX_NAME!r} has dimension "
        f"{index_description.dimension}; expected {EMBEDDING_DIMENSION} for "
        "gemini-embedding-001. Create a compatible index and re-index the "
        "repository."
    )

index = pinecone.Index(INDEX_NAME)
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    api_key=_required_env("GOOGLE_API_KEY"),
)
sparse_encoder = BM25Encoder().default()


def store_chunks(chunks, replace=False):
    if not chunks:
        print("No chunks to store")
        return

    documents = [chunk["content"] for chunk in chunks]
    dense_vectors = embedding_model.embed_documents(documents)
    sparse_vectors = sparse_encoder.encode_documents(documents)
    if len(dense_vectors) != len(chunks) or len(sparse_vectors) != len(chunks):
        raise RuntimeError("Embedding services returned an incomplete vector set")

    vectors = []
    for chunk, dense_vector, sparse_vector in zip(
        chunks, dense_vectors, sparse_vectors
    ):
        file_path = chunk["file_path"]
        vector_id = (
            f"{file_path}:{chunk['start_line']}:{chunk['type']}:"
            f"{chunk.get('name') or ''}"
        )
        vectors.append(
            {
                "id": vector_id,
                "values": dense_vector,
                "sparse_values": sparse_vector,
                "metadata": {
                    "file_path": file_path,
                    "type": chunk["type"],
                    "name": chunk.get("name") or "",
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "content": chunk["content"],
                },
            }
        )

    if replace:
        clear_namespace()

    for offset in range(0, len(vectors), 100):
        index.upsert(
            vectors=vectors[offset : offset + 100],
            namespace=NAMESPACE,
        )

    print(f"Stored {len(vectors)} hybrid chunks in Pinecone")


def clear_namespace():
    if not NAMESPACE:
        raise ValueError(
            "PINECONE_NAMESPACE must be set before clearing indexed data"
        )
    index.delete(delete_all=True, namespace=NAMESPACE)


def _scale_query(dense_vector, sparse_vector):
    dense_norm = math.sqrt(sum(value * value for value in dense_vector))
    if dense_norm == 0:
        raise ValueError("Dense query embedding has zero magnitude")

    return (
        [
            value * HYBRID_ALPHA / dense_norm
            for value in dense_vector
        ],
        {
            "indices": sparse_vector["indices"],
            "values": [
                value * (1 - HYBRID_ALPHA)
                for value in sparse_vector["values"]
            ],
        },
    )


def searchCode(query, n_result=5):
    dense_vector = embedding_model.embed_query(query)
    sparse_vector = sparse_encoder.encode_queries(query)
    dense_vector, sparse_vector = _scale_query(dense_vector, sparse_vector)

    return index.query(
        vector=dense_vector,
        sparse_vector=sparse_vector,
        namespace=NAMESPACE,
        top_k=n_result,
        include_metadata=True,
    )
