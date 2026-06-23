import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from rag.reranker import rerank

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

index = faiss.read_index(
    "rag/vector_store/index.faiss"
)

with open(
    "rag/vector_store/chunks.pkl",
    "rb"
) as f:
    chunks = pickle.load(f)

with open(
    "rag/vector_store/metadata.pkl",
    "rb"
) as f:
    metadata = pickle.load(f)


def retrieve(query, k=10):

    embedding = model.encode(
        [query]
    )

    embedding = np.array(
        embedding
    ).astype("float32")

    distances, indices = index.search(
        embedding,
        k
    )

    results = []

    for idx in indices[0]:

        results.append(
            {
                "text": chunks[idx],
                "source": metadata[idx]["source"]
            }
        )

    reranked_results = rerank(
        query,
        results,
        top_k=3
    )

    return reranked_results