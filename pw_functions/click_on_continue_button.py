import asyncio
import logging
import random

from playwright.async_api import Page

from config import LOG_FILE, SECONDS_TIMEOUT

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


async def click_on_continue_button(page: Page):
    """Click the 'Continue' button."""
    continue_button = page.locator("xpath=//button[@type='submit']")
    await continue_button.wait_for(timeout=SECONDS_TIMEOUT * 1000)  # Convert to ms

    # Scroll into view
    await continue_button.scroll_into_view_if_needed()
    await asyncio.sleep(random.uniform(0.5, 1))

    # Move to and click the button
    await continue_button.hover()
    await asyncio.sleep(random.uniform(0.5, 1))
    await continue_button.click()

    logger.info("Clicked on 'Submit' button")
