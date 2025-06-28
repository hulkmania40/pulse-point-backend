from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import event_routes, timeline_routes

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        # Uncomment the following lines to enable CORS for these origins
        # "https://pulse-point.onrender.com/",
        # "http://localhost:5173"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_routes.router)
app.include_router(timeline_routes.router)
