import asyncio
import logging
import random

from playwright.async_api import Page, Browser

from config import LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


async def search_person_script(page: Page):
    """Search for 'Confirming you are a real person' message."""
    logger.info("Search for 'Confirming you are a real person'")
    try:
        # Wait for the text to appear
        real_person_text = page.locator(
            "xpath=//*[contains(text(), 'you are a real person')]"
        )
        await real_person_text.wait_for(timeout=10_000)

        # Simulate mouse movements
        await page.mouse.move(90, 90)
        await asyncio.sleep(random.uniform(0.2, 0.5))
        await page.mouse.move(70, 110)  # Adjusted for -20, 20 relative movement
        await asyncio.sleep(random.uniform(0.3, 0.9))

        # Wait 30 seconds
        await asyncio.sleep(30)

    except Exception:
        pass  # Silently continue on timeout or failure, as in original
