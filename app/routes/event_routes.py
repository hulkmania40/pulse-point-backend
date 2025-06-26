from fastapi import APIRouter, HTTPException
from app.models.event_model import EventModel
from app.crud.event_crud import *

router = APIRouter()

@router.get("/events", response_model=list[EventModel])
async def list_events():
    return await get_all_events()

@router.post("/events", response_model=EventModel)
async def create(event: EventModel):
    return await create_event(event.dict(by_alias=True, exclude={"id"}))

@router.get("/events/{event_id}", response_model=EventModel)
async def get(event_id: str):
    event = await get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}", response_model=EventModel)
async def update(event_id: str, event: EventModel):
    return await update_event(event_id, event.dict(by_alias=True, exclude={"id"}))
