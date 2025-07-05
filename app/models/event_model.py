from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
from app.models.common import PyObjectId

class EventInputModel(BaseModel):
    title: str
    slug: str
    tags: List[str]
    description: Optional[str] = None
    coverImage: Optional[str] = None
    published: bool = True
    dateCreated: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    dateUpdated: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class EventModel(EventInputModel):
    id: PyObjectId = Field(alias="_id")