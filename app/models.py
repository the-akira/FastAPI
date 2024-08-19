from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from typing import List, Optional

# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head

class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None

class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)

class ScrapedData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str]
    meta_description: Optional[str]
    headings: Optional[List[str]] = Field(sa_column=Column(JSON))
    links: Optional[List[str]] = Field(sa_column=Column(JSON))
    content: Optional[List[str]] = Field(sa_column=Column(JSON))