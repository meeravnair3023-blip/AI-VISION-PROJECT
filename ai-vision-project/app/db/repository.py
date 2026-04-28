# Import DB session (connection handler)
from app.db.session import SessionLocal

# Import Product model
from app.db.models import Product


# Function to fetch product by item_name
def get_product(item_name: str):

    # 🔹 Create new DB session (connection)
    db = SessionLocal()

    # 🔹 Query database
    # SELECT * FROM products WHERE item_name = ?
    result = db.query(Product).filter(
    Product.item_name.ilike(f"%{item_name}%")
).first()

    # 🔹 Close DB connection (VERY IMPORTANT)
    db.close()

    # 🔹 Return result (either Product object or None)
    return result