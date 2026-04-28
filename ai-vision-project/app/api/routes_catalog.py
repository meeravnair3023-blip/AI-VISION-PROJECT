# 🔹 Import FastAPI router (used to define API endpoints)
from fastapi import APIRouter

# 🔹 Import DB repository function (handles DB queries)
from app.db.repository import get_product

# 🔹 Import Pydantic schema (used for response validation)
from app.schemas.product import Product

# 🔹 Create router instance (registered in main.py)
router = APIRouter()


# 🔹 API Endpoint: Get product from catalog
# Example: GET /api/v1/catalog/laptop
# response_model=Product → ensures output follows Product schema
@router.get("/catalog/{item_name}", response_model=Product)
def get_item(item_name: str):

    # 🔹 Call DB layer to fetch product by item_name
    product = get_product(item_name)

    # 🔹 Return product object
    # FastAPI automatically:
    #   ✔ Converts SQLAlchemy object → JSON
    #   ✔ Validates response using Product schema
    return product