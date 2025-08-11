# :Modules: Authentication Router
# [[ Purpose - User registration and login endpoints. ]]
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

# Import dependencies, schemas, models, security functions
from app.api import deps
from app.core.security import create_access_token, get_password_hash
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token

# Authentication Router.
router = APIRouter(tags=["Authentication"])


# === Register New User ===
@router.post("/register", response_model=UserRead)

# === User Login ===