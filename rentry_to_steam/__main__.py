import asyncio

from .http_session import HTTPSession
from . import ARGS

async def main():
    http = HTTPSession()
    await http.start()

    for rentry_url in ARGS.urls:
        workshop_ids = await http.get_workshop_ids(rentry_url)
        app_id = await http.get_app_id(list(workshop_ids.values())[0])

        for workshop_name, workshop_id in workshop_ids.items():
            success = await http.subscribe(workshop_id, app_id)

            if success:
                print(f"[SUBSCRIBED] {workshop_name} {workshop_id}")

            else:
                print(f"[SUBSCRIBE FAIL] {workshop_name} {workshop_id}")

if __name__ == "__main__":
    asyncio.run(main())