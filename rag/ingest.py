import os
import pickle
import numpy as np
import faiss

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_FOLDER = "documents/PDFs"
VECTOR_FOLDER = "rag/vector_store"

os.makedirs(VECTOR_FOLDER, exist_ok=True)

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

documents = []
metadata = []

for file in os.listdir(PDF_FOLDER):

    if file.endswith(".pdf"):

        pdf_path = os.path.join(
            PDF_FOLDER,
            file
        )

        print(f"Reading {file}")

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        chunks = splitter.split_text(text)

        for chunk in chunks:

            documents.append(chunk)

            metadata.append(
                {
                    "source": file
                }
            )

print(f"Total chunks: {len(documents)}")

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

embeddings = np.array(
    embeddings
).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    embeddings
)

faiss.write_index(
    index,
    "rag/vector_store/index.faiss"
)

with open(
    "rag/vector_store/chunks.pkl",
    "wb"
) as f:
    pickle.dump(
        documents,
        f
    )

with open(
    "rag/vector_store/metadata.pkl",
    "wb"
) as f:
    pickle.dump(
        metadata,
        f
    )

print("Vector database created successfully.")