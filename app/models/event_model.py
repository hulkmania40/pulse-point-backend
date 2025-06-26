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


class EventModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    title: str
    slug: str
    tags: List[str]
    description: Optional[str] = None
    coverImage: Optional[str] = None
    published: bool = True
    dateCreated: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    dateUpdated: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True
