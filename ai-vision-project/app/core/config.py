# Import os (used later if you want to load environment variables)
import os


# Central configuration class
# This holds all important settings for your application
#  Keeps config in ONE place (very important for maintainability)
class Settings:

    #  Database connection string
    # Format: mysql+driver://username:password@host/db_name
    # This is used by SQLAlchemy to connect to MySQL
    DB_URL = "mysql+mysqlconnector://root:root123@localhost/vision_price"

    # AI model name (Ollama)
    # Currently using "llava" (vision model)
    # You can change this later to:
    #    "llama3" (text)
    #    or switch to Gemini without touching API code
    OLLAMA_MODEL = "llava"

    #  Base URL where Ollama server is running
    # Default Ollama runs on localhost:11434
    OLLAMA_BASE_URL = "http://localhost:11434"


# Create a global settings object
# This is imported everywhere in your project
#  Example: from app.core.config import settings
settings = Settings()