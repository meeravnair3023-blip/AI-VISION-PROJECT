# Import router
from fastapi import APIRouter

# Create router
router = APIRouter()

# Health check endpoint
# Example: GET /api/v1/health
@router.get("/health")
def health():
    # Used to check if API is running
    return {"status": "ok"}