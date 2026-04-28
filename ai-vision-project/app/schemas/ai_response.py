# Import Pydantic base class for data validation
from pydantic import BaseModel

# Import typing helpers
from typing import List, Optional


# 🔹 AI Detection Response Schema
# 👉 This validates the JSON returned by the AI model (Ollama / Gemini)
class AIDetectionResponse(BaseModel):

    # Whether AI successfully recognized the item
    recognized: bool

    # Normalized item name (used for DB lookup)
    # Example: "laptop"
    item_name: Optional[str]

    # User-friendly name
    # Example: "Dell Laptop"
    display_name: Optional[str]

    # Category of item
    # Example: "electronics"
    category: Optional[str]

    # Alternative names (for future fuzzy matching)
    # Example: ["notebook", "computer"]
    aliases: List[str] = []

    # Confidence score (0.0 → 1.0)
    confidence: float

    # Whether human verification is needed
    # Useful for low-confidence cases
    needs_human_review: bool = False

    # Message from AI explaining result
    message: str


# 🔹 Final API Response Schema
# 👉 This is what your FastAPI returns to UI (Gradio / Flutter)
class RecognitionAPIResponse(BaseModel):

    # Overall API status
    # "success" | "not_found" | "error"
    status: str

    # Whether item was recognized
    recognized: bool

    # Normalized item name
    item_name: Optional[str]

    # Display name
    display_name: Optional[str]

    # Category
    category: Optional[str]

    # Price from DB
    price: Optional[float]

    # Currency (INR)
    currency: Optional[str]

    # Confidence from AI
    confidence: float

    # Source of request
    # "image_upload" | "live_feed"
    source: str

    # Error code (if any)
    # Example: "ITEM_NOT_RECOGNIZED"
    error_code: Optional[str]

    # Final message to user
    message: str