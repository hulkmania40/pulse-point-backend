from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls): yield cls.validate
    @classmethod
    def validate(cls, v): return ObjectId(v) if ObjectId.is_valid(v) else ValueError("Invalid ObjectId")
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string", "format": "objectid"}


class TimelineItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    eventId: PyObjectId  # Reference to Event
    date: str
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
        json_encoders = {ObjectId: str}
        populate_by_name = True
