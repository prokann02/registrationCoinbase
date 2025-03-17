import asyncio
import logging
import random

from playwright.async_api import Page


async def search_person_script(page: Page):
    """Search for 'Confirming you are a real person' message."""
    logger = logging.getLogger()

    logger.info("Search for 'Confirming you are a real person'")
    try:
        real_person_text = page.locator(
            "xpath=//*[contains(text(), 'you are a real person')]"
        )
        await real_person_text.wait_for(timeout=10_000)

        # Simulate mouse movements
        await page.mouse.move(90, 90)
        await asyncio.sleep(random.uniform(0.2, 0.5))
        await page.mouse.move(70, 110)
        await asyncio.sleep(random.uniform(0.3, 0.9))

        await asyncio.sleep(40)

    except Exception:
        pass
