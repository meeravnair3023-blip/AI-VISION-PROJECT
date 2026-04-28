# Import SQLAlchemy engine creator
from sqlalchemy import create_engine

# Import session maker
from sqlalchemy.orm import sessionmaker

# Import DB config
from app.core.config import settings


# 🔹 Create database engine (connection pool)
# This connects Python → MySQL
engine = create_engine(settings.DB_URL)


# 🔹 Create session factory
#  Used to create DB sessions in repository
SessionLocal = sessionmaker(bind=engine)