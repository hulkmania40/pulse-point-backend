from fastapi import APIRouter, HTTPException
from app.models.event_model import EventModel
from app.models.timeline_model import TimelineEventRequest, TimelineItemModel, UpdateTimelineEventRequest
from app.crud.timeline_crud import *

router = APIRouter()

@router.get("/events/{event_id}/timeline", response_model=TimelineEventRequest)
async def get_timeline_for_event(event_id: str):
    return await fetch_timeline_event_data(event_id)

@router.post("/timeline")
async def create_timeline_event(payload: TimelineEventRequest):
    return await create_timeline_events(payload.dict())

@router.put("/timeline")
async def update_timeline_event(payload: UpdateTimelineEventRequest):
    return await update_timeline_events(payload.dict())

@router.get("/timeline/{item_id}", response_model=TimelineItemModel)
async def get_item(item_id: str):
    item = await get_timeline_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Timeline item not found")
    return item

@router.delete("/timeline/{item_id}")
async def delete_item(item_id: str):
    res = await delete_timeline_item(item_id)
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted successfully"}
