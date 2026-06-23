def build_context(docs):

    context = ""

    for i, doc in enumerate(docs):

        context += f"""
Evidence {i+1}

Source: {doc["source"]}

Relevance Score: {doc["score"]:.2f}

{doc["text"]}

--------------------------------
"""

    return context