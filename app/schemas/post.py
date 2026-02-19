from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    title: str
    slug: str                       # URL-friendly identifier, e.g. "my-first-post"
    excerpt: str                    # short summary shown in the list
    content: str                    # full Markdown content
    tags: List[str] = []
    cover_url: Optional[str] = None
    published: bool = False         # drafts won't appear in public endpoints


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    cover_url: Optional[str] = None
    published: Optional[bool] = None


class PostOut(PostBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
