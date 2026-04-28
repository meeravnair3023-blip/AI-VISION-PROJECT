# 🔹 Import DB session (connection handler)
from app.db.session import SessionLocal

# 🔹 Import Product model (table)
from app.db.models import Product


# 🔹 Advanced product lookup function
# Now supports BOTH:
#    - item_name (e.g., "laptop")
#    - brand (e.g., "acer")
def find_product(item_name: str, brand: str = None):

    # 🔹 Create DB session
    db = SessionLocal()

    try:
        # 🔹 Base query (search by item_name using partial match)
        query = db.query(Product).filter(
            Product.item_name.ilike(f"%{item_name}%")
        )

        # 🔥 Optional: filter by brand if available
        if brand:
            query = query.filter(
                Product.brand.ilike(f"%{brand}%")
            )

        # 🔹 Get first matching product
        result = query.first()

        return result

    finally:
        # 🔹 Always close DB connection
        db.close()