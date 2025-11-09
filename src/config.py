import os
from dotenv import load_dotenv

load_dotenv()

# Core paths
REPO_URL = os.getenv("REPO_URL")
REPO_PATH = os.getenv("REPO_PATH")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")

# LLM selection
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").lower()
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
# LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#ingest
SUPPORTED_FILE_TYPES = os.getenv("SUPPORTED_FILE_TYPES", ".java").split(",")

# Processing parameters
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 2000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

# Validation
if LLM_PROVIDER not in {"openai", "google"}:
    raise ValueError("LLM_PROVIDER must be 'openai' or 'google'")
