# 🔹 Import SQLAlchemy column types
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

# 🔹 Base class for all database models (tables)
# Every table must inherit from this
from sqlalchemy.orm import declarative_base

# 🔹 Used to generate timestamps automatically
from sqlalchemy.sql import func


# 🔹 Create base class
Base = declarative_base()


# 🔹 Product Model (maps to "products" table in MySQL)
class Product(Base):

    # 🔹 Table name in database
    __tablename__ = "products"


    # 🔹 Primary Key (unique identifier)
    id = Column(Integer, primary_key=True)


    # 🔹 Normalized product name (used for matching)
    # Example: "laptop", "mouse"
    # index=True → speeds up search queries
    item_name = Column(String, index=True)


    # 🔹 User-friendly display name
    # Example: "Dell Laptop 15 inch"
    display_name = Column(String)


    # 🔹 SKU (Stock Keeping Unit)
    # Unique product identifier (optional but useful)
    sku = Column(String)


    # 🔹 Product category
    # Example: "electronics"
    # index=True → improves filtering performance
    category = Column(String, index=True)


    # 🔹 Product price
    price = Column(Float)


    # 🔹 Currency type
    # Default = INR (as per your PRD)
    currency = Column(String, default="INR")


    # 🔹 Indicates whether product is active
    # Useful for soft delete / disabling products
    is_active = Column(Boolean, default=True)


    # 🔹 Timestamp of last update
    # server_default → sets value when row is created
    # onupdate → automatically updates on modification
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    brand = Column(String, index=True)