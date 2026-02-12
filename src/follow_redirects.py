import asyncio

from playwright.async_api import async_playwright


class PlaywrightBrowser:

    def __init__(self, playwright, browser):
        self._playwright = playwright
        self._browser = browser

    @classmethod
    async def initialize(cls, headless: bool = True):
        """Initialize Playwright, browser, and tools."""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=headless)
        return cls(playwright, browser)

    def get_browser(self):
        return self._browser

    async def teardown(self):
        """Gracefully close browser and playwright."""
        await self._browser.close()
        await self._playwright.stop()


async def _follow_redirects_async(url: str) -> str:
    from urllib.parse import urlparse
    initial_host = urlparse(url).netloc
    browser = await PlaywrightBrowser.initialize(headless=True)
    try:
        page = await browser.get_browser().new_page()
        await page.goto(url, wait_until="domcontentloaded")
        try:
            await page.wait_for_url(
                lambda current: urlparse(current).netloc != initial_host,
                timeout=10000,
            )
        except Exception:
            pass
        return page.url
    finally:
        await browser.teardown()


def follow_redirects(url: str) -> str:
    """Follow redirects for a given URL and return the final URL.

    Args:
        url: The initial URL to follow redirects from.
    Returns:
        The final URL after following redirects.
    """
    return asyncio.run(_follow_redirects_async(url))