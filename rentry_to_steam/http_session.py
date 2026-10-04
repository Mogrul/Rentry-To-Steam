from http.cookiejar import MozillaCookieJar
from urllib.parse import urlparse, parse_qs
from wsgiref import headers

import httpx
from bs4 import BeautifulSoup


class HTTPSession:
    def __init__(self):
        self._session: httpx.AsyncClient | None = None

    @property
    def session(self) -> httpx.AsyncClient:
        if self._session is None:
            raise RuntimeError("HTTPX session isn't started")

        return self._session

    async def start(self):
        if self._session:
            return

        jar = MozillaCookieJar()
        jar.load(".cookies/steam.txt", ignore_discard=True, ignore_expires=True)

        for cookie in jar:
            cookie.expires = None

        self._session = httpx.AsyncClient(
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                              "AppleWebKit/537.36 (KHTML, like Gecko)"
                              "Chrome/154.0.0.0 Safari/537.36",
            }
        )
        self._session.cookies.update(jar)

    async def get(self, url: str, **kwargs) -> httpx.Response:
        response = await self.session.get(url, **kwargs)

        print(f"[{response.status_code}] {response.url}")

        return response

    async def post(self, url: str, **kwargs) -> httpx.Response:
        response = await self.session.post(url, **kwargs)

        print(f"[{response.status_code}] {response.url}")

        return response

    async def get_app_id(self, workshop_id: int) -> int | None:
        response = await self.session.post(
            "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/",
            data={
                "itemcount": 1,
                "publishedfileids[0]": workshop_id
            },
        )
        if response.status_code != 200:
            return None

        details = response.json()["response"]["publishedfiledetails"][0]
        app_id = details.get("consumer_app_id") or details.get("consumer_appid")
        return int(app_id) if app_id else None

    async def get_workshop_ids(self, rentry_url: str) -> dict[str, int]:
        workshop_ids: dict[str, int] = {}

        response = await self.get(rentry_url)

        if response.status_code != 200:
            return workshop_ids

        page = BeautifulSoup(response.text, "html.parser")

        external_tags = page.find_all("a", class_="external")
        for external_tag in external_tags:
            href = external_tag.get("href")

            if not isinstance(href, str):
                continue

            parsed = urlparse(href)
            params = parse_qs(parsed.query)

            workshop_slug = params.get("id")

            if not isinstance(workshop_slug, list):
                continue

            workshop_slug = workshop_slug[0]
            workshop_id = workshop_slug.split(" ")[0]
            workshop_package_name = workshop_slug.split(" ")[-1]

            workshop_ids[workshop_package_name] = int(workshop_id)

        return workshop_ids

    async def subscribe(self, workshop_id: int, app_id: int | None = None) -> bool:
        if app_id is None:
            app_id = await self.get_app_id(workshop_id)
            if app_id is None:
                print(f"Failed to retrieve App ID from Workshop ID {workshop_id}")
                return False

        session_id = self.session.cookies.get("sessionid", domain="steamcommunity.com")
        if not session_id:
            raise RuntimeError("No steamcommunity.com sessionid cookies found")

        response = await self.post(
            "https://steamcommunity.com/sharedfiles/subscribe",
            data={
                "id": workshop_id,
                "appid": app_id,
                "sessionid": session_id,
            },
            headers={
                "Origin": "https://steamcommunity.com",
                "Referer": f"https://steamcommunity.com/sharedfiles/filedetails/?id={workshop_id}"
            }
        )

        if response.status_code != 200:
            return False

        return response.json().get("success") == 1

        return False