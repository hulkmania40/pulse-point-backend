from fastapi import APIRouter, HTTPException
from app.models.event_model import EventModel
from app.models.timeline_model import TimelineEventRequest, TimelineItemModel, UpdateTimelineEventRequest
from app.crud.timeline_crud import *

router = APIRouter()

@router.get("/events/{event_id}/timeline", response_model=TimelineEventRequest)
async def get_timeline_for_event(event_id: str):
    return await fetch_timeline_event_data(event_id)

@router.post("/timeline/add")
async def create_timeline_event(payload: TimelineEventRequest):
    return await create_timeline_events(payload.dict(by_alias=True, exclude_unset=True))

@router.put("/timeline")
async def update_timeline_event(payload: UpdateTimelineEventRequest):
    return await update_timeline_events(payload.dict())

@router.delete("/timeline/{item_id}")
async def delete_item(item_id: str):
    res = await delete_timeline_item(item_id)
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted successfully"}
