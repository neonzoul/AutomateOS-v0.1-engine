# :Modules: Database Session & Engine
# [[ Database Dependency ]]
import os

from sqlmodel import create_engine, Session, SQLModel

# === Defines Database File ===
# DB Path/name.db
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
db_file_path = os.path.join(project_root, "database.db")

DATABASE_URL = f'sqlite:///{db_file_path}'  # ?Replace with actual database URL in a .env file later

# === Create Engine ===
engine = create_engine(DATABASE_URL, echo=True)

# Dependency for API Endpoints
def get_session():
    with Session(engine) as session:
        yield session

# Function for main.py called on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)