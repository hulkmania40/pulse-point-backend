from app.database import db
from app.models.event_model import EventModel
from bson import ObjectId
import datetime

event_collection = db["events"]

async def get_all_events():
    events = await event_collection.find({"published": True}).sort("dateUpdated", -1).to_list(100)
    return [EventModel(**e) for e in events]

async def create_event(event: dict):
    event["dateCreated"] = event["dateUpdated"] = datetime.datetime.utcnow()
    res = await event_collection.insert_one(event)
    return await get_event(str(res.inserted_id))

async def get_event(event_id: str):
    data = await event_collection.find_one({"_id": ObjectId(event_id)})
    return EventModel(**data) if data else None

async def update_event(event_id: str, update: dict):
    update["dateUpdated"] = datetime.datetime.utcnow()
    await event_collection.update_one({"_id": ObjectId(event_id)}, {"$set": update})
    return await get_event(event_id)
