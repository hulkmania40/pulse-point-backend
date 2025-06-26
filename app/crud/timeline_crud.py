from app.database import db
from app.models.timeline_model import TimelineItemModel
from bson import ObjectId
import datetime

timeline_collection = db["timelines"]
event_collection = db["events"]

async def get_timeline(event_id: str):
    cursor = timeline_collection.find({"eventId": ObjectId(event_id)}).sort("date", -1)
    result = await cursor.to_list(length=100)
    return [TimelineItemModel(**doc) for doc in result]

async def create_timeline_item(item: dict):
    item["eventId"] = ObjectId(item["eventId"])
    item["dateCreated"] = item["dateUpdated"] = datetime.datetime.utcnow()
    res = await timeline_collection.insert_one(item)

    # Update parent event's dateUpdated
    await event_collection.update_one(
        {"_id": item["eventId"]},
        {"$set": {"dateUpdated": datetime.datetime.utcnow()}}
    )

    return await get_timeline_item(str(res.inserted_id))

async def get_timeline_item(item_id: str):
    doc = await timeline_collection.find_one({"_id": ObjectId(item_id)})
    return TimelineItemModel(**doc) if doc else None

async def update_timeline_item(item_id: str, update: dict):
    update["dateUpdated"] = datetime.datetime.utcnow()
    await timeline_collection.update_one({"_id": ObjectId(item_id)}, {"$set": update})

    # Update the parent event's last modified time
    updated_doc = await timeline_collection.find_one({"_id": ObjectId(item_id)})
    if updated_doc:
        await event_collection.update_one(
            {"_id": updated_doc["eventId"]},
            {"$set": {"dateUpdated": datetime.datetime.utcnow()}}
        )

    return await get_timeline_item(item_id)

async def delete_timeline_item(item_id: str):
    return await timeline_collection.delete_one({"_id": ObjectId(item_id)})
