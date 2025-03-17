import itertools
import logging
import sys

import requests
from playwright.async_api import Page

from config import SELECTED_AGENT
from helpers.save_screenshot import save_screenshot

PROXIES = None
proxy_cycle = None
_SELECTED_PROXY = None


class SelectedProxy:
    def __init__(self):
        self._current = next(proxy_cycle) if PROXIES else None

    @property
    def current(self):
        if self._current is None:
            raise ValueError("No proxy available yet")
        return self._current

    def next(self):
        if proxy_cycle is None:
            raise ValueError("Proxy cycle not initialized")
        self._current = next(proxy_cycle)
        return self._current

    def get_proxies(self):
        if self._current is None:
            raise ValueError("No proxy available yet")
        return {
            "http": self._current,
            "https": self._current,
        }


async def get_proxy(proxy_file):
    """Finds a working proxy from the list."""
    logger = logging.getLogger()

    global PROXIES, proxy_cycle, _SELECTED_PROXY

    with open(proxy_file, 'r') as f:
        PROXIES = [line.strip() for line in f.readlines()]

    if not PROXIES:
        logger.error("Proxy file is empty. Continuing without proxy!")
        proxy_file = None
        return proxy_file

    proxy_cycle = itertools.cycle(PROXIES)
    _SELECTED_PROXY = SelectedProxy()

    attempts = 0
    max_attempts = len(PROXIES)

    headers = {
        "User-Agent": SELECTED_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, async deflate, br",
        "Connection": "keep-alive",
    }

    session = requests.Session()

    while attempts < max_attempts:
        proxy = _SELECTED_PROXY.current
        logger.info(f"Testing proxy {attempts + 1}/{max_attempts}: {proxy}")

        proxies = _SELECTED_PROXY.get_proxies()

        try:
            response = session.get(
                "https://example.com",
                proxies=proxies,
                headers=headers,
                timeout=20,
                allow_redirects=False,
            )
            if response.status_code == 200:
                logger.info(f"Proxy {proxy} works with HTTPS")
                return proxy
            else:
                logger.warning(f"Proxy {proxy} returned status {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Proxy {proxy} failed: {str(e)}")

        _SELECTED_PROXY.next()
        attempts += 1

    logger.error("No working proxies found after trying all available options")
    sys.exit(0)


def get_selected_proxy():
    if _SELECTED_PROXY is None:
        raise ValueError("Proxy not initialized yet. Call get_proxy first.")
    return _SELECTED_PROXY


async def search_oops_page(page: Page, browser):
    logger = logging.getLogger(__name__)

    # Check for "Oops" text variations
    oops_text = page.locator(
        "xpath=//*[contains(text(), 'Oops')]"
    )

    not_found = "Did not find 'Welcome' or 'Oops' text, continuing"

    try:
        await oops_text.wait_for(timeout=5_000)  # 5 seconds timeout
        if await oops_text.is_visible():
            logger.info("Found 'Oops' text on the page - possible human verification")
            # Optionally save screenshot for debugging
            await save_screenshot(text="found 'Oops' page", page=page)

            if _SELECTED_PROXY is not None:
                old_proxy = _SELECTED_PROXY.current
                new_proxy = _SELECTED_PROXY.next()
                logger.info(f"Switching proxy from {old_proxy} to {new_proxy}")

                await browser.close()
                return 1

            else:
                logger.warning("No proxy available to switch to")
                exit(1)
        else:
            logger.info(not_found)
            return None
    except Exception:
        logger.info(not_found)
        return None
