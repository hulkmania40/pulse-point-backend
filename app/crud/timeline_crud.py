from fastapi import HTTPException
from app.models.event_model import EventModel
from database import db
from app.models.timeline_model import TimelineItemModel
from typing import List
from bson import ObjectId
import datetime

timeline_collection = db["timelines"]
events_collection = db["events"]

async def fetch_timeline_event_data(event_id: str):
    try:
        obj_id = ObjectId(event_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid eventId format")

    try:
        print("SUPERMAN" * 10)
        print(event_id)

        # Get the event document
        event_data = await events_collection.find_one({"_id": obj_id})
        print("-" * 50)
        print(event_data)

        if not event_data:
            raise HTTPException(status_code=404, detail="Event not found")

        # Convert _id to eventId
        event_data["eventId"] = str(event_data.pop("_id"))

        # Timeline query
        print("$" * 50)
        timeline_docs = await timeline_collection.find({"eventId": obj_id}).to_list(length=None)

        # Convert ObjectIds to strings
        for doc in timeline_docs:
            doc["_id"] = str(doc["_id"])
            doc["eventId"] = str(doc["eventId"])

        return {
            "eventDetails": event_data,
            "timeLinesDetails": timeline_docs
        }

    except Exception as e:
        print("🔥 ERROR OCCURRED 🔥")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


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

async def update_timeline_events(data: dict):
    
    event_id = ObjectId(data["eventId"])
    event_data = data["event_data"]
    timelines_data = data["timelines_data"]

    # Update timestamps
    now = datetime.datetime.utcnow()
    event_data["dateUpdated"] = now

    # Update event in events collection
    await events_collection.update_one(
        {"_id": event_id},
        {"$set": event_data}
    )

    # Remove old timeline entries linked to this eventId
    await timeline_collection.delete_many({"eventId": event_id})

    # Insert updated timeline entries
    for timeline in timelines_data:
        timeline["eventId"] = event_id
        timeline["dateCreated"] = timeline["dateUpdated"] = now

    if timelines_data:
        await timeline_collection.insert_many(timelines_data)

    return {
        "message": "Event and timelines updated successfully",
        "eventId": str(event_id),
        "timelineCount": len(timelines_data)
    }


async def delete_timeline_item(item_id: str):
    await events_collection.delete_many({"eventId": ObjectId(item_id)})
    await timeline_collection.delete_one({"_id": ObjectId(item_id)})