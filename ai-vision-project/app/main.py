from fastapi import FastAPI

# 🔹 Import all route modules
# Each file contains a group of APIs (modular design)
from app.api import routes_recognition, routes_health, routes_catalog


# 🔹 Create FastAPI application instance
# This is the main backend app (entry point)
app = FastAPI()


# 🔹 Register Recognition APIs
# All routes inside routes_recognition.py will be prefixed with /api/v1
# Example:
# /recognize/image → becomes → /api/v1/recognize/image
app.include_router(routes_recognition.router, prefix="/api/v1")


# 🔹 Register Health API
# Example:
# /health → becomes → /api/v1/health
app.include_router(routes_health.router, prefix="/api/v1")


# 🔹 Register Catalog APIs
# Example:
# /catalog/{item_name} → becomes → /api/v1/catalog/{item_name}
app.include_router(routes_catalog.router, prefix="/api/v1")