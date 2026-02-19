from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.schemas.post import PostCreate, PostUpdate, PostOut
from app.core.supabase import get_supabase
from app.core.security import require_auth
from supabase import Client

router = APIRouter()
TABLE = "blog_posts"


# ── PUBLIC ────────────────────────────────────────────────────────

@router.get("/", response_model=List[PostOut])
def list_posts(
    tag: Optional[str] = Query(None),
    db: Client = Depends(get_supabase),
):
    """List all published posts. Publicly accessible."""
    res = (
        db.table(TABLE)
        .select("*")
        .eq("published", True)
        .order("created_at", desc=True)
        .execute()
    )
    data = res.data or []
    if tag:
        data = [p for p in data if tag in (p.get("tags") or [])]
    return data


@router.get("/{slug}", response_model=PostOut)
def get_post(slug: str, db: Client = Depends(get_supabase)):
    """Get a single published post by slug. Publicly accessible."""
    res = (
        db.table(TABLE)
        .select("*")
        .eq("slug", slug)
        .eq("published", True)
        .single()
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Post not found")
    return res.data


# ── PROTECTED (JWT required) ──────────────────────────────────────

@router.post("/", response_model=PostOut, status_code=201)
def create_post(
    payload: PostCreate,
    db: Client = Depends(get_supabase),
    _auth: dict = Depends(require_auth),      # 🔒 token required
):
    """Create a post. Admin only."""
    existing = db.table(TABLE).select("id").eq("slug", payload.slug).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="Slug already exists")
    res = db.table(TABLE).insert(payload.model_dump()).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create post")
    return res.data[0]


@router.patch("/{post_id}", response_model=PostOut)
def update_post(
    post_id: str,
    payload: PostUpdate,
    db: Client = Depends(get_supabase),
    _auth: dict = Depends(require_auth),      # 🔒 token required
):
    """Update a post. Admin only."""
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    res = db.table(TABLE).update(updates).eq("id", post_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Post not found")
    return res.data[0]


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: str,
    db: Client = Depends(get_supabase),
    _auth: dict = Depends(require_auth),      # 🔒 token required
):
    """Delete a post. Admin only."""
    res = db.table(TABLE).delete().eq("id", post_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Post not found")
