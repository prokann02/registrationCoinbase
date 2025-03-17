import logging
import sys

from playwright.async_api import Page, Browser
from playwright.async_api import Playwright

from config import SECONDS_TIMEOUT, SELECTED_AGENT
from helpers.get_proxy import get_selected_proxy


async def start_browser(playwright: Playwright, proxy_file) -> tuple[Browser, Page]:
    """Creates a browser instance with the given settings and added cookies."""
    logger = logging.getLogger()

    try:
        launch_args = {
            "headless": False,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-ipc-flooding-protection",
                "--no-first-run",
                "--password-store=basic",
                "--ignore-certificate-errors",
                f"--user-agent={SELECTED_AGENT}",
            ],
            "timeout": SECONDS_TIMEOUT * 1000,  # Convert to milliseconds
        }

        if proxy_file:
            selected_proxy = get_selected_proxy()
            current = selected_proxy.current
            if current:
                server = selected_proxy.get_proxies()["https"]

                # If proxy has username and password
                if "@" in current:
                    parts = current.rsplit("@")[0].split("://")[1].split(":")
                    username, password = parts[0], parts[1]
                    proxy_config = {
                        "server": server,
                        "username": username,
                        "password": password,
                    }
                else:
                    proxy_config = {
                        "server": server,
                    }

                launch_args["proxy"] = proxy_config

        # Launch Chromium browser
        browser = await playwright.chromium.launch(**launch_args)

        # Create a new page
        page = await browser.new_page(
            viewport={"width": 1800, "height": 1200},
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9"
            },
            ignore_https_errors=True
        )

        # Additional configuration to hide automation
        await page.evaluate("""
                            Object.defineProperty(navigator, 'webdriver', {
                                get: () => undefined
                            });
                        """)

        logger.info("Browser successfully started")

        return browser, page

    except Exception as e:
        logger.error(f"Browser startup error: {e}")
        sys.exit(0)
