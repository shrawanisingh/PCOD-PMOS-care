from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, documents, top_k=3):

    pairs = []

    for doc in documents:

        pairs.append(
            (
                query,
                doc["text"]
            )
        )

    scores = reranker.predict(
        pairs
    )

    scored_docs = []

    for score, doc in zip(scores, documents):

        scored_docs.append(
            (
                score,
                doc
            )
        )

    scored_docs.sort(
        key=lambda x: x[0],
        reverse=True
    )

    reranked = []

    for score, doc in scored_docs[:top_k]:

        doc["score"] = float(score)

        reranked.append(doc)

    return reranked