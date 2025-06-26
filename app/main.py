from fastapi import FastAPI
from app.routes import event_routes, timeline_routes

app = FastAPI()

app.include_router(event_routes.router)
app.include_router(timeline_routes.router)
