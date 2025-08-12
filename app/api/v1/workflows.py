from fastapi import APIRouter, Depends
from .deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["Test deps with workflows"])

# Test create workflows enpoint with Guard dependency.
@router.post("/workflows")
def create_workflow(
    *,
    current_user: User = Depends(get_current_user) # "Guard"
):
    
    return{"message": f"Workflow created by user {current_user}"}