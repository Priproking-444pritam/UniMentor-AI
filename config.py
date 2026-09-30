"""
UniMentor AI - Configuration
============================
Loads the Groq API key from the .env file and stores
all application-level constants in one place.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# API CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL = "llama-3.3-70b-versatile"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ============================================================
# RETRIEVAL CONFIGURATION
# ============================================================

CHUNK_SIZE = 700
CHUNK_OVERLAP = 100
TOP_K = 5

# Minimum cosine similarity a chunk must have to be treated
# as relevant. Chunks below this are discarded so the model
# is not handed unrelated text.
SIMILARITY_THRESHOLD = 0.25

DOCUMENTS_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "documents",
)

# ============================================================
# DEPARTMENTS / AGENTS
# ============================================================

DEPARTMENTS = [
    "curriculum",
    "placement",
    "scholarship",
]

CATEGORY_TO_DEPARTMENT = {
    "CURRICULUM": "curriculum",
    "PLACEMENT": "placement",
    "SCHOLARSHIP": "scholarship",
    "GENERAL": None,
}

AGENT_NAMES = {
    "CURRICULUM": "Curriculum Agent",
    "PLACEMENT": "Placement Agent",
    "SCHOLARSHIP": "Scholarship Agent",
    "GENERAL": "General Academic Agent",
}

NOT_FOUND_MESSAGE = (
    "I could not find this information in the available "
    "university documents. Please check with the academic "
    "office or your faculty advisor."
)

# ============================================================
# VALIDATION
# ============================================================

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Create a .env file and add:\n"
        "GROQ_API_KEY=your_groq_api_key_here"
    )
