import asyncio
import datetime
import sys
import os

# Ensure access to app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import db  # assumes you have `app/database.py` with `db` exported

# Collections
event_collection = db["events"]
timeline_collection = db["timelines"]

now = datetime.datetime.utcnow()

# --------------------------
# Space Race Event & Timeline
# --------------------------
space_race = {
    "title": "Space Race",
    "slug": "space-race",
    "tags": ["space", "cold war", "technology"],
    "description": "A Cold War competition between the US and USSR for dominance in space exploration (1955-1975).",
    "coverImage": "https://picsum.photos/seed/space-race/600/400",
    "published": True,
    "dateCreated": now,
    "dateUpdated": now,
}

space_race_timeline = [
    {
        "date": "October 4, 1957",
        "title": "Sputnik 1 Launched",
        "subtitle": "First artificial satellite",
        "status": "Milestone",
        "location": "Baikonur Cosmodrome, USSR",
        "countryName": "Soviet Union",
        "countryCode": "RU",
        "imageUrl": "https://picsum.photos/500?random=301",
        "imageCaption": "Sputnik 1 in orbit illustration.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "Roscosmos",
        "events": [
            "USSR launches the first artificial satellite.",
            "Start of the space race.",
            "Shocked and motivated the United States."
        ]
    },
    {
        "date": "April 12, 1961",
        "title": "Yuri Gagarin Orbits Earth",
        "subtitle": "First human in space",
        "status": "Historic Flight",
        "location": "Baikonur to Earth Orbit",
        "countryName": "Soviet Union",
        "countryCode": "RU",
        "imageUrl": "https://picsum.photos/500?random=302",
        "imageCaption": "Yuri Gagarin before launch.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "Russian Archives",
        "events": [
            "Yuri Gagarin becomes first human to orbit Earth.",
            "Flight lasted 108 minutes.",
            "Vostok 1 mission boosted USSR prestige."
        ]
    },
    {
        "date": "July 20, 1969",
        "title": "Apollo 11 Moon Landing",
        "subtitle": "First humans on the Moon",
        "status": "Victory",
        "location": "Moon",
        "countryName": "United States",
        "countryCode": "US",
        "imageUrl": "https://picsum.photos/500?random=303",
        "imageCaption": "Neil Armstrong on the lunar surface.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "NASA",
        "events": [
            "Neil Armstrong and Buzz Aldrin land on the Moon.",
            "Fulfills JFK’s 1961 goal.",
            "\"One small step for man...\" moment broadcast worldwide."
        ]
    },
    {
        "date": "May 24, 1972",
        "title": "Apollo-Soyuz Agreement",
        "subtitle": "Shift toward cooperation",
        "status": "Transition",
        "location": "Washington D.C.",
        "countryName": "United States",
        "countryCode": "US",
        "imageUrl": "https://picsum.photos/500?random=304",
        "imageCaption": "Handshake in space planning begins.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "NASA Archives",
        "events": [
            "US and USSR agree to conduct joint space missions.",
            "Leads to 1975 Apollo-Soyuz Test Project.",
            "Symbolic end to intense rivalry."
        ]
    }
]

async def seed_space_race():
    try:
        # Optional: delete previous version
        # await event_collection.delete_many({"slug": "space-race"})
        # await timeline_collection.delete_many({"slug": {"$exists": False}, "eventId": {"$exists": True}})

        # Insert main event
        result = await event_collection.insert_one(space_race)
        event_id = result.inserted_id

        # Insert timeline items
        for item in space_race_timeline:
            item["eventId"] = event_id
            item["dateCreated"] = now
            item["dateUpdated"] = now
        await timeline_collection.insert_many(space_race_timeline)

        print("✅ Space Race seeding complete!")

    except Exception as e:
        print("❌ Seeding failed:", e)

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_space_race())
