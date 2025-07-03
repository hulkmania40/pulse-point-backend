from app.models.event_model import EventModel
from database import db
from app.models.timeline_model import TimelineItemModel
from bson import ObjectId
import datetime

timeline_collection = db["timelines"]
events_collection = db["events"]

async def get_timeline(event_id: str):
    cursor = timeline_collection.find({"eventId": ObjectId(event_id)}).sort("date", -1)
    result = await cursor.to_list(length=100)
    return [TimelineItemModel(**doc) for doc in result]

from typing import List
from bson import ObjectId
import datetime

async def create_timeline_events(data: dict):
    timelines_data: List[dict] = data["timeLinesDetails"]
    event_data: dict = data["eventDetails"]

    # Add timestamps to event_data
    now = datetime.datetime.utcnow()
    event_data["dateCreated"] = event_data["dateUpdated"] = now

    # Insert event_data, MongoDB generates _id
    event_result = await events_collection.insert_one(event_data)
    generated_event_id = event_result.inserted_id  # This is the new ObjectId

    # Attach generated_event_id to each timeline item
    for timeline in timelines_data:
        timeline["eventId"] = generated_event_id
        timeline["dateCreated"] = timeline["dateUpdated"] = now

    # Insert all timeline items into 'timelines' collection
    if timelines_data:
        await timeline_collection.insert_many(timelines_data)

    return {
        "message": "Event and timeline entries created successfully",
        "eventId": str(generated_event_id),
        "timelineCount": len(timelines_data),
    }

async def get_timeline_item(item_id: str):
    doc = await timeline_collection.find_one({"_id": ObjectId(item_id)})
    return TimelineItemModel(**doc) if doc else None

async def update_timeline_item(item_id: str, update: dict):
    update["dateUpdated"] = datetime.datetime.utcnow()
    await timeline_collection.update_one({"_id": ObjectId(item_id)}, {"$set": update})

    # Update the parent event's last modified time
    updated_doc = await timeline_collection.find_one({"_id": ObjectId(item_id)})
    if updated_doc:
        await events_collection.update_one(
            {"_id": updated_doc["eventId"]},
            {"$set": {"dateUpdated": datetime.datetime.utcnow()}}
        )

    return await get_timeline_item(item_id)

async def delete_timeline_item(item_id: str):
    return await timeline_collection.delete_one({"_id": ObjectId(item_id)})
