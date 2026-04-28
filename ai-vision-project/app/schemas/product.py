# Import Pydantic
from pydantic import BaseModel


# 🔹 Product schema (used for API responses / data transfer)
class Product(BaseModel):

    # Normalized name (used internally)
    item_name: str

    # Display name (for UI)
    display_name: str

    # Category
    category: str

    # Price
    price: float

    # Currency
    currency: str