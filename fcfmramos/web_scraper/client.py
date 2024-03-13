import asyncio
import aiohttp
import atexit
import random
from typing import Tuple
from bs4 import BeautifulSoup


def load_cookies(path: str) -> dict:
    cookies = {}

    with open(path, "r") as file:
        cookie_key_values = file.read().split(";")

    for cookie in cookie_key_values:
        key, value = cookie.split("=")
        key = key.strip()
        value = value.strip()
        cookies[key] = value

    return cookies


class Client:
    _timeout_protection = False
    _timeout_protection_time = (0.1, 0.5)

    def __init__(self, cookies: dict = {}) -> None:
        self._session = aiohttp.ClientSession(cookies=cookies)
        atexit.register(self._close)

    def enable_timeout_protection(
        self, min_time: float = 0.1, max_time: float = 0.5
    ) -> None:
        self._timeout_protection = True
        self._timeout_protection_time = (min_time, max_time)

    def disable_timeout_protection(self) -> None:
        self._timeout_protection = False

    async def get(self, url: str) -> Tuple[int, str]:
        if self._timeout_protection:
            await asyncio.sleep(random.uniform(0.1, 0.5))  # nosec
        async with self._session.get(url) as response:
            return (response.status, await response.text())

    async def scrape(self, url: str) -> BeautifulSoup:
        response_code, html = await self.get(url)
        if response_code != 200:
            print(f"Failed to fetch {url} with response code {response_code}")
        return BeautifulSoup(html, "html.parser")

    def _close(self) -> None:
        asyncio.run(self._session.close())
