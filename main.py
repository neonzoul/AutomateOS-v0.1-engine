# :Modules: FastAPI Application Entrypoint

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import create_db_and_tables
from app.api.v1.endpoints import auth


# === Lifespan (startup/shutdown) ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Automate OS Engine...")
    create_db_and_tables()
    print("Database tables created successfully")
    print("🕹️  API Documentation: http://127.0.0.1:8000/docs")
    print("🕳️  Alternative docs: http://127.0.0.1:8000/redoc")
    
    yield
    
    # SHUTDOWN
    print("Shutting down Automate OS Engine...")
    # [[Add any cleanup code here -- For example: close database connections, cleanup resources, etc.]]
    print("Cleanup completed") # [[ needed ?]]
    
# === FastAPI Application Setup ===
app = FastAPI(
    title="AutomateOS", 
	version="0.2.0",
    lifespan=lifespan
)

# === Router Registration ===
# [[ Include authentication router with API versioning ]]
# [[ All auth endpoints will be available under /api/v1/* prefix ]]
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])

# === Root Endpoint ===
@app.get("/")
def read_root():
    return {"message": "AutomateOS Engine is running"}