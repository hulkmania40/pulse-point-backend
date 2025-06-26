from fastapi import APIRouter, HTTPException
from app.models.timeline_model import TimelineItemModel
from app.crud.timeline_crud import *

router = APIRouter()

@router.get("/events/{event_id}/timeline", response_model=list[TimelineItemModel])
async def get_timeline_for_event(event_id: str):
    return await get_timeline(event_id)

@router.post("/events/{event_id}/timeline", response_model=TimelineItemModel)
async def create_timeline(event_id: str, item: TimelineItemModel):
    item_dict = item.dict(by_alias=True, exclude={"id"})
    item_dict["eventId"] = event_id
    return await create_timeline_item(item_dict)

@router.get("/timeline/{item_id}", response_model=TimelineItemModel)
async def get_item(item_id: str):
    item = await get_timeline_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Timeline item not found")
    return item

@router.put("/timeline/{item_id}", response_model=TimelineItemModel)
async def update_item(item_id: str, item: TimelineItemModel):
    return await update_timeline_item(item_id, item.dict(by_alias=True, exclude={"id"}))

@router.delete("/timeline/{item_id}")
async def delete_item(item_id: str):
    res = await delete_timeline_item(item_id)
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted successfully"}
