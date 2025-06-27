import asyncio
import datetime
import sys
import os

# Access project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import db  # Make sure app/database.py exists and exports `db`

# Collections
event_collection = db["events"]
timeline_collection = db["timelines"]

now = datetime.datetime.utcnow()

# --------------------------
# Cold War Event & Timeline
# --------------------------
cold_war = {
    "title": "Cold War",
    "slug": "cold-war",
    "tags": ["cold war", "geopolitics", "superpowers", "20th century"],
    "description": "A period of political and military tension between the US and USSR from 1947 to 1991.",
    "coverImage": "https://picsum.photos/seed/cold-war/600/400",
    "published": True,
    "dateCreated": now,
    "dateUpdated": now,
}

cold_war_timeline = [
    {
        "date": "March 12, 1947",
        "title": "Truman Doctrine Announced",
        "subtitle": "Start of containment policy",
        "status": "Policy Shift",
        "location": "Washington, D.C.",
        "countryName": "United States",
        "countryCode": "US",
        "imageUrl": "https://picsum.photos/500?random=401",
        "imageCaption": "President Truman addressing Congress.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "US National Archives",
        "events": [
            "President Truman promises support to countries threatened by communism.",
            "Marks beginning of official US policy of containment.",
            "Set the stage for Cold War geopolitical alignment."
        ]
    },
    {
        "date": "June 24, 1948",
        "title": "Berlin Blockade Begins",
        "subtitle": "First major Cold War crisis",
        "status": "Tension",
        "location": "Berlin, Germany",
        "countryName": "Germany",
        "countryCode": "DE",
        "imageUrl": "https://picsum.photos/500?random=402",
        "imageCaption": "Supplies dropped during Berlin Airlift.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "Bundesarchiv",
        "events": [
            "USSR blocks Western access to West Berlin.",
            "US and allies respond with Berlin Airlift.",
            "Over 200,000 flights delivered food and fuel."
        ]
    },
    {
        "date": "October 16–28, 1962",
        "title": "Cuban Missile Crisis",
        "subtitle": "Closest to nuclear war",
        "status": "Crisis",
        "location": "Cuba / Washington / Moscow",
        "countryName": "United States",
        "countryCode": "US",
        "imageUrl": "https://picsum.photos/500?random=403",
        "imageCaption": "Recon photo of Soviet missile installation in Cuba.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "CIA",
        "events": [
            "US discovers Soviet missiles in Cuba.",
            "13 days of intense negotiation follow.",
            "Ends with USSR agreeing to withdraw missiles."
        ]
    },
    {
        "date": "November 9, 1989",
        "title": "Fall of the Berlin Wall",
        "subtitle": "Symbolic end of Cold War",
        "status": "Breakthrough",
        "location": "Berlin, Germany",
        "countryName": "Germany",
        "countryCode": "DE",
        "imageUrl": "https://picsum.photos/500?random=404",
        "imageCaption": "Berliners celebrating as the wall falls.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "Deutsche Welle",
        "events": [
            "East Germany opens border after protests.",
            "Crowds dismantle the Berlin Wall.",
            "Paves the way for German reunification."
        ]
    },
    {
        "date": "December 26, 1991",
        "title": "Dissolution of the Soviet Union",
        "subtitle": "Formal end of Cold War",
        "status": "Collapse",
        "location": "Moscow, USSR",
        "countryName": "Soviet Union",
        "countryCode": "RU",
        "imageUrl": "https://picsum.photos/500?random=405",
        "imageCaption": "Soviet flag lowered for the last time.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "RIA Novosti",
        "events": [
            "USSR officially ceases to exist.",
            "15 independent republics emerge.",
            "Marks the end of Cold War era."
        ]
    }
]

async def seed_cold_war():
    try:
        # await event_collection.delete_many({"slug": "cold-war"})
        # await timeline_collection.delete_many({"slug": {"$exists": False}, "eventId": {"$exists": True}})

        result = await event_collection.insert_one(cold_war)
        event_id = result.inserted_id

        for item in cold_war_timeline:
            item["eventId"] = event_id
            item["dateCreated"] = now
            item["dateUpdated"] = now

        await timeline_collection.insert_many(cold_war_timeline)
        print("✅ Cold War seeding complete!")

    except Exception as e:
        print("❌ Seeding failed:", e)

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_cold_war())
