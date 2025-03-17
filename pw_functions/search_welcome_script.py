import asyncio
import logging
import random

from playwright.async_api import Page

from helpers.save_screenshot import save_screenshot


async def search_welcome_script(page: Page):
    """Check for 'Welcome! Who are you creating this account for?' and select 'Individual'."""
    logger = logging.getLogger(__name__)

    try:
        # Wait for the welcome text to appear
        welcome_text = page.locator(
            "xpath=//*[contains(text(), 'Welcome! Who are you creating this account for?')]"
        )
        await welcome_text.wait_for(timeout=20 * 1000)  # Convert to milliseconds

        # Simulate mouse movements
        await page.mouse.move(120, 120)
        await asyncio.sleep(random.uniform(0.6, 1.1))

        logger.info("Found 'Welcome! Who are you creating this account for?' text")

        # Find the div with "Individual" text and locate its clickable parent <a>
        individual_div = page.locator("xpath=//div[contains(text(), 'Individual')]")
        await individual_div.wait_for(timeout=10_000)  # 10 seconds in milliseconds

        # Go up to the nearest clickable <a> ancestor
        individual_link = individual_div.locator("xpath=ancestor::a")
        await individual_link.wait_for(state="visible", timeout=10_000)

        await save_screenshot(text="discovering 'Welcome' page", page=page)

        # Move to and click the link
        await individual_link.hover()  # Simulate mouse movement to element
        await individual_link.click()
        logger.info("Selected 'Individual' option by clicking the parent <a>")
        await asyncio.sleep(random.uniform(0.5, 1))

    except Exception:
        logger.info("Did not find 'Welcome! Who are you creating this account for?' text, continue")
