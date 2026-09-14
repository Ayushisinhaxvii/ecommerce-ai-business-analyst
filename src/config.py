# Import Path so we can create reliable project paths
from pathlib import Path

# Import os so we can read environment variables
import os

# Import dotenv so Python can load values from our .env file
from dotenv import load_dotenv


# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Define the important project folders
DATA_PATH = PROJECT_ROOT / "data"
PROCESSED_DATA_PATH = DATA_PATH / "processed"
DOCS_PATH = PROJECT_ROOT / "docs"


# Define the SQLite database path
DATABASE_PATH = PROCESSED_DATA_PATH / "ecommerce.db"


# Define the FAISS vector database folder
VECTOR_DB_PATH = PROCESSED_DATA_PATH / "faiss_index"


# Define the saved FAISS index file
FAISS_INDEX_PATH = VECTOR_DB_PATH / "mercato.index"


# Define the saved document chunks file
CHUNKS_PATH = VECTOR_DB_PATH / "chunks.pkl"


# Load the .env file from the project root
load_dotenv(PROJECT_ROOT / ".env")


# Read the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Read the Gemini model
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)