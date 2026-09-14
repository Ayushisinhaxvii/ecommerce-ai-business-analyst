# Import Path so we can work with project files and folders
from pathlib import Path

# Import pickle so we can save and load document chunks
import pickle

# Import FAISS for vector similarity search
import faiss

# Import NumPy for working with embedding vectors
import numpy as np

# Import Sentence Transformer for creating embeddings
from sentence_transformers import SentenceTransformer

# Import LangChain's Document object
from langchain_core.documents import Document

# Import the text splitter used to divide documents into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import the FAISS and chunk paths from our configuration
from src.config import (
    FAISS_INDEX_PATH,
    CHUNKS_PATH,
    PROJECT_ROOT
)


# Load the embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Create a function that builds the FAISS index
def build_faiss_index():

    # Define the folder containing our company documents
    docs_path = PROJECT_ROOT / "docs"

    # Find all Markdown documents
    markdown_files = list(
        docs_path.glob("*.md")
    )

    # Create an empty list for our documents
    documents = []


    # Read every Markdown document
    for file in markdown_files:

        # Read the saved document text
        text = file.read_text(
            encoding="utf-8"
        )

        # Create a LangChain Document
        document = Document(
            page_content=text,
            metadata={
                "source": str(file)
            }
        )

        # Add the document to our list
        documents.append(document)


    # Create the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )


    # Split the documents into smaller chunks
    chunks = text_splitter.split_documents(
        documents
    )


    # Extract text from every chunk
    chunk_texts = [
        chunk.page_content
        for chunk in chunks
    ]


    # Convert chunks into embedding vectors
    chunk_embeddings = embedding_model.encode(
        chunk_texts,
        show_progress_bar=False
    )


    # Convert embeddings into the format required by FAISS
    embedding_matrix = np.asarray(
        chunk_embeddings,
        dtype="float32"
    )


    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(
        embedding_matrix
    )


    # Get the embedding dimension
    embedding_dimension = (
        embedding_matrix.shape[1]
    )


    # Create a FAISS index using inner-product similarity
    index = faiss.IndexFlatIP(
        embedding_dimension
    )


    # Add the document embeddings to FAISS
    index.add(
        embedding_matrix
    )


    # Create the FAISS folder if it doesn't exist
    FAISS_INDEX_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # Save the FAISS index
    faiss.write_index(
        index,
        str(FAISS_INDEX_PATH)
    )


    # Save the document chunks
    with open(
        CHUNKS_PATH,
        "wb"
    ) as file:

        # Store the chunks and metadata
        pickle.dump(
            chunks,
            file
        )


    # Return the index and chunks
    return index, chunks


# Check whether the saved FAISS files already exist
if (
    FAISS_INDEX_PATH.exists()
    and CHUNKS_PATH.exists()
):

    # Load the existing FAISS index
    loaded_index = faiss.read_index(
        str(FAISS_INDEX_PATH)
    )


    # Load the saved document chunks
    with open(
        CHUNKS_PATH,
        "rb"
    ) as file:

        # Read the chunks from disk
        loaded_chunks = pickle.load(
            file
        )


# Build the RAG index if the files don't exist
else:

    # Create the FAISS index and document chunks
    loaded_index, loaded_chunks = (
        build_faiss_index()
    )


# Create a function that retrieves relevant chunks
def retrieve(
    query,
    top_k=3
):

    # Convert the user's question into an embedding
    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")


    # Normalize the question embedding
    faiss.normalize_L2(
        query_embedding
    )


    # Search for the most relevant chunks
    scores, indices = loaded_index.search(
        query_embedding,
        top_k
    )


    # Create a list for the retrieved results
    results = []


    # Match every FAISS result with its document chunk
    for rank, chunk_index in enumerate(
        indices[0]
    ):

        # Get the corresponding chunk
        chunk = loaded_chunks[
            chunk_index
        ]


        # Store the chunk and similarity score
        results.append(
            {
                "chunk": chunk,
                "score": float(
                    scores[0][rank]
                )
            }
        )


    # Return the retrieved results
    return results