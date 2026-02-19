from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class ProjectBase(BaseModel):
    title: str
    description: str
    tags: List[str] = []
    image_url: Optional[str] = None
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    featured: bool = False
    order: int = 0                  # display order (lower = first)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    featured: Optional[bool] = None
    order: Optional[int] = None


class ProjectOut(ProjectBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
