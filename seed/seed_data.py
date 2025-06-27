import asyncio
import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import db

# Collections
event_collection = db["events"]
timeline_collection = db["timelines"]

now = datetime.datetime.utcnow()

# --------------------
# WW1 Main Event & Timeline
# --------------------
ww1 = {
    "title": "World War 1",
    "slug": "world-war-1",
    "tags": ["war", "ww1", "global"],
    "description": "A global war from 1914-1918.",
    "coverImage": "https://picsum.photos/seed/ww1/600/400",
    "published": True,
    "dateCreated": now,
    "dateUpdated": now,
}

ww1_data = [
    {
        "date": "June 28, 1914",
        "title": "Assassination of Archduke Franz Ferdinand",
        "subtitle": "Spark that ignited the war",
        "status": "Trigger Event",
        "location": "Sarajevo, Bosnia",
        "countryName": "Bosnia and Herzegovina",
        "countryCode": "BA",
        "imageUrl": "https://picsum.photos/500?random=1",
        "imageCaption": "Gavrilo Princip, assassin of Archduke Franz Ferdinand.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "Wikimedia Commons",
        "events": [
            "Archduke Franz Ferdinand of Austria-Hungary was assassinated.",
            "Gavrilo Princip, a Bosnian Serb nationalist, carried out the attack.",
            "This incident triggered diplomatic crises across Europe."
        ]
    },
    {
        "date": "1915",
        "title": "Trench Warfare Begins",
        "subtitle": "Western Front solidifies",
        "status": "Stalemate",
        "location": "Western Front",
        "countryName": "France",
        "countryCode": "FR",
        "imageUrl": "https://picsum.photos/500?random=3",
        "imageCaption": "German trench on the Western Front.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "Bundesarchiv (Germany)",
        "events": [
            "Massive trench systems constructed across France and Belgium.",
            "Battle of Gallipoli begins; heavy Allied casualties.",
            "Poison gas used for the first time in warfare."
        ]
    },
    {
        "date": "1919",
        "title": "Treaty of Versailles",
        "subtitle": "Post-war settlement",
        "status": "War Ends Formally",
        "location": "Versailles, France",
        "countryName": "France",
        "countryCode": "FR",
        "imageUrl": "https://picsum.photos/500?random=7",
        "imageCaption": "World leaders at the signing of the Treaty of Versailles.",
        "imageType": "AI_GENERATED",
        "imageSource": "Wikimedia Commons",
        "events": [
            "Germany forced to accept full responsibility for the war.",
            "Heavy reparations and territorial losses imposed on Germany.",
            "League of Nations was established to prevent future conflicts."
        ]
    }
]

ww1_additional = [
    {
        "date": "1916",
        "title": "Battle of Verdun",
        "subtitle": "Longest battle of WWI",
        "status": "Major Battle",
        "location": "Verdun, France",
        "countryName": "France",
        "countryCode": "FR",
        "imageUrl": "https://picsum.photos/500?random=101",
        "imageCaption": "Soldiers in the trenches at Verdun.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "French Archives",
        "events": [
            "Fought between France and Germany.",
            "Over 700,000 casualties in total.",
            "Symbol of French determination and suffering."
        ]
    },
    {
        "date": "1917",
        "title": "Russian Revolution",
        "subtitle": "Russia exits the war",
        "status": "Political Shift",
        "location": "Petrograd, Russia",
        "countryName": "Russia",
        "countryCode": "RU",
        "imageUrl": "https://picsum.photos/500?random=102",
        "imageCaption": "Revolutionaries in Petrograd.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "Russian State Archives",
        "events": [
            "Bolsheviks overthrow the provisional government.",
            "Russia withdraws from WWI.",
            "Leads to civil war and eventual rise of the USSR."
        ]
    }
]

# --------------------
# WW2 Main Event & Timeline
# --------------------
ww2 = {
    "title": "World War 2",
    "slug": "world-war-2",
    "tags": ["war", "ww2", "global"],
    "description": "A global war from 1939–1945.",
    "coverImage": "https://picsum.photos/seed/ww2/600/400",
    "published": True,
    "dateCreated": now,
    "dateUpdated": now,
}

ww2_data = [
    {
        "date": "September 1, 1939",
        "title": "Invasion of Poland",
        "subtitle": "Start of WWII",
        "status": "War Begins",
        "location": "Poland",
        "countryName": "Poland",
        "countryCode": "PL",
        "imageUrl": "https://picsum.photos/500?random=10",
        "imageCaption": "German tanks entering Poland.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "Bundesarchiv",
        "events": [
            "Germany invades Poland using blitzkrieg tactics.",
            "This marks the official beginning of World War II.",
            "Britain and France declare war on Germany."
        ]
    },
    {
        "date": "June 6, 1944",
        "title": "D-Day Landings",
        "subtitle": "Allies land in Normandy",
        "status": "Turning Point",
        "location": "Normandy, France",
        "countryName": "France",
        "countryCode": "FR",
        "imageUrl": "https://picsum.photos/500?random=11",
        "imageCaption": "Troops landing at Normandy on D-Day.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "U.S. Army",
        "events": [
            "Allied forces launch Operation Overlord.",
            "Largest amphibious invasion in history.",
            "Opened a new Western front against Germany."
        ]
    },
    {
        "date": "May 8, 1945",
        "title": "Victory in Europe Day",
        "subtitle": "Germany surrenders",
        "status": "Victory",
        "location": "Berlin, Germany",
        "countryName": "Germany",
        "countryCode": "DE",
        "imageUrl": "https://picsum.photos/500?random=12",
        "imageCaption": "Celebrations across Allied nations.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "BBC Archives",
        "events": [
            "Germany unconditionally surrenders.",
            "End of World War II in Europe.",
            "Mass celebrations and relief worldwide."
        ]
    }
]

ww2_additional = [
    {
        "date": "August 6, 1945",
        "title": "Hiroshima Bombing",
        "subtitle": "First use of atomic bomb",
        "status": "Nuclear Attack",
        "location": "Hiroshima, Japan",
        "countryName": "Japan",
        "countryCode": "JP",
        "imageUrl": "https://picsum.photos/500?random=201",
        "imageCaption": "Mushroom cloud over Hiroshima.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "U.S. Archives",
        "events": [
            "US drops atomic bomb on Hiroshima.",
            "Over 100,000 people killed.",
            "Leads to Japan's surrender."
        ]
    },
    {
        "date": "September 2, 1945",
        "title": "Formal Surrender of Japan",
        "subtitle": "End of World War II",
        "status": "Surrender",
        "location": "Tokyo Bay, Japan",
        "countryName": "Japan",
        "countryCode": "JP",
        "imageUrl": "https://picsum.photos/500?random=202",
        "imageCaption": "Signing of surrender aboard USS Missouri.",
        "imageType": "ACTUAL_PICTURE",
        "imageSource": "National Archives",
        "events": [
            "Japan signs surrender aboard USS Missouri.",
            "World War II officially ends.",
            "Start of US occupation of Japan."
        ]
    }
]

ww1_timeline = ww1_data + ww1_additional
ww2_timeline = ww2_data + ww2_additional

async def seed():
    try:
        # await event_collection.delete_many({})
        # await timeline_collection.delete_many({})

        ww1_result = await event_collection.insert_one(ww1)
        ww1_id = ww1_result.inserted_id

        for item in ww1_timeline:
            item["eventId"] = ww1_id
            item["dateCreated"] = now
            item["dateUpdated"] = now
        await timeline_collection.insert_many(ww1_timeline)

        ww2_result = await event_collection.insert_one(ww2)
        ww2_id = ww2_result.inserted_id

        for item in ww2_timeline:
            item["eventId"] = ww2_id
            item["dateCreated"] = now
            item["dateUpdated"] = now
        await timeline_collection.insert_many(ww2_timeline)

        print("✅ Seed successful!")

    except Exception as e:
        print("❌ Seeding failed:", e)

asyncio.run(seed())

if __name__ == "__main__":
    asyncio.run(seed())