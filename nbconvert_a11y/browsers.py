"""playwright tools."""

from contextlib import AsyncExitStack
from dataclasses import field
from os import PathLike
from dataclasses import dataclass
from playwright.async_api import Browser, async_playwright, Playwright


@dataclass
class Browser:
    context: Playwright = None
    stack: AsyncExitStack = field(default_factory=AsyncExitStack)
    browser: Browser = None

    async def __aenter__(self):
        self.context = await self.stack.enter_async_context(async_playwright())
        self.browser = await self.context.chromium.launch()
        return self

    async def __aexit__(self, exc, typ, tb):
        await self.stack.aclose()

    @classmethod
    async def pages(cls, *urls, **config):
        async with cls() as self:
            async for page in self.goto(*urls, **config):
                yield page

    async def goto(self=None, *urls, **config):
        for url in urls:
            page = await self.browser.new_page()
            if isinstance(url, PathLike):
                url = url.absolute().as_uri()
            await page.goto(url)
            yield page
