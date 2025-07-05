from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

from app.models.common import PyObjectId
from app.models.event_model import EventInputModel

class TimelineItemInputModel(BaseModel):
    eventId: Optional[PyObjectId] = None
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

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

class TimelineItemModel(TimelineItemInputModel):
    id: PyObjectId = Field(alias="_id")

class TimelineEventRequest(BaseModel):
    eventDetails: EventInputModel
    timeLinesDetails: List[TimelineItemInputModel]

class UpdateTimelineEventRequest(TimelineEventRequest):
    eventId: str