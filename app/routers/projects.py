from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.core.supabase import get_supabase
from app.core.security import require_auth
from supabase import Client

router = APIRouter()
TABLE = "projects"


# ── PUBLIC ────────────────────────────────────────────────────────

@router.get("/", response_model=List[ProjectOut])
def list_projects(
    featured: Optional[bool] = Query(None),
    tag: Optional[str]       = Query(None),
    db: Client = Depends(get_supabase),
):
    """List all projects. Publicly accessible."""
    query = db.table(TABLE).select("*").order("order", desc=False)
    if featured is not None:
        query = query.eq("featured", featured)
    data = query.execute().data or []
    if tag:
        data = [p for p in data if tag in (p.get("tags") or [])]
    return data


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: str, db: Client = Depends(get_supabase)):
    """Get a single project by ID. Publicly accessible."""
    res = db.table(TABLE).select("*").eq("id", project_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return res.data


# ── PROTECTED (JWT required) ──────────────────────────────────────

@router.post("/", response_model=ProjectOut, status_code=201)
def create_project(
    payload: ProjectCreate,
    db: Client = Depends(get_supabase),
    _auth: dict = Depends(require_auth),      # 🔒 token required
):
    """Create a project. Admin only."""
    res = db.table(TABLE).insert(payload.model_dump()).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create project")
    return res.data[0]


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    db: Client = Depends(get_supabase),
    _auth: dict = Depends(require_auth),      # 🔒 token required
):
    """Update a project. Admin only."""
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    res = db.table(TABLE).update(updates).eq("id", project_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return res.data[0]


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: str,
    db: Client = Depends(get_supabase),
    _auth: dict = Depends(require_auth),      # 🔒 token required
):
    """Delete a project. Admin only."""
    res = db.table(TABLE).delete().eq("id", project_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Project not found")
