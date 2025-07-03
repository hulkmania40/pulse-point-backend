from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

from app.models.common import PyObjectId
from app.models.event_model import EventModel  # ✅ Import shared PyObjectId

class TimelineItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    eventId: PyObjectId  # Reference to parent event
    date: datetime.datetime
    title: str
    subtitle: Optional[str] = None
    status: Optional[str] = None
    location: Optional[str] = None
    countryName: Optional[str] = None
    countryCode: Optional[str] = None
    imageUrl: Optional[str] = None
    imageCaption: Optional[str] = None
    imageType: Optional[str] = None
    imageSource: Optional[str] = None
    events: List[str] = []
    dateCreated: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    dateUpdated: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

class TimelineEventRequest(BaseModel):
    eventDetails: EventModel
    timeLinesDetails: List[TimelineItemModel]