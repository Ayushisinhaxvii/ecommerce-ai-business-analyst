# Import pickle so we can load our saved document chunks
import pickle

# Import FAISS so we can search our vector database
import faiss

# Import NumPy for working with vectors
import numpy as np

# Import Sentence Transformer for creating embeddings
from sentence_transformers import SentenceTransformer

# Import paths for our saved RAG files
from src.config import (
    FAISS_INDEX_PATH,
    CHUNKS_PATH
)


# Load the saved FAISS index
loaded_index = faiss.read_index(
    str(FAISS_INDEX_PATH)
)


# Load the saved document chunks
with open(CHUNKS_PATH, "rb") as file:

    # Restore the original LangChain documents
    loaded_chunks = pickle.load(file)


# Load the same embedding model used when creating the index
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Retrieve the most relevant company-document chunks
def retrieve(query, top_k=3):

    # Convert the user's question into an embedding
    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    # Normalize the query for cosine similarity
    faiss.normalize_L2(query_embedding)

    # Search for the most relevant chunks
    scores, indices = loaded_index.search(
        query_embedding,
        top_k
    )

    # Create a list for the retrieved results
    results = []

    # Loop through the retrieved chunks
    for rank, chunk_index in enumerate(indices[0]):

        # Ignore invalid FAISS indexes
        if chunk_index < 0:
            continue

        # Get the corresponding document chunk
        chunk = loaded_chunks[chunk_index]

        # Save the chunk and similarity score
        results.append(
            {
                "chunk": chunk,
                "score": float(scores[0][rank])
            }
        )

    # Return the retrieved documents
    return results