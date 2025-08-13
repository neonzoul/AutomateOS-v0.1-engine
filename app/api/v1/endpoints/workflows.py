# Workflow API CRUD Endpoints
from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.v1.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, WorkflowRead

router = APIRouter()

# === Create Workflow ===
@router.post("/", response_model=WorkflowRead)
async def create_workflow(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    workflow_in: WorkflowCreate
) -> WorkflowRead:
    db_workflow = Workflow.model_validate(workflow_in, update={"user_id": current_user.id})

    session.add(db_workflow)
    session.commit()
    session.refresh(db_workflow)
    return WorkflowRead.model_validate(db_workflow)
# [[ for invalid Input or Request FastAPI will handle Error ]]

# === Read Workflow ===

# --- Read List---
@router.get("/", response_model=List[WorkflowRead]) # [[ "/" == "/api/v1/workflows/" | Type List for return multiple objects.(workflows)]]
async def read_workflow(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> List[WorkflowRead]:
    # [[ Retrieve all workflows for the current user. ]]
    workflows = session.exec(
        select(Workflow).where(Workflow.user_id == current_user.id)
    ).all()
    return [WorkflowRead.model_validate(w) for w in workflows]  # [[ Explicitly convert each DB model to its corresponding Pydantic schema. ]]

# --- Read Single by ID ---
@router.get("/{workflow_id}", response_model=WorkflowRead)
async def read_sigle_workflow(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    workflow_id: int
):
    # [[ Retireve sigle workflow by workflow ID ]]
    # Fetch workflow
    workflow = session.get(Workflow, workflow_id)

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    # Check the workflow belong to current user.
    # [[ protect other user's workflow ID ]]
    if workflow.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    return workflow