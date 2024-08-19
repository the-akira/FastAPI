from pydantic import BaseModel
from typing import Optional

class ScrapeRequest(BaseModel):
    url: str

class SongCreate(BaseModel):
    name: str
    artist: str
    year: Optional[int] = None

class EmailRequest(BaseModel):
    email: str
    subject: str
    message: str