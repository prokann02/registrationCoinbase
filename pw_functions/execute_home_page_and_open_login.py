import asyncio
import logging
import random

from playwright.async_api import Page, Browser

from config import LOG_FILE
from config import SECONDS_TIMEOUT, COINBASE_MAIN_URL
from helpers.save_screenshot import save_screenshot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


async def execute_home_page_and_open_login(page: Page):
    """Visit the main page for cookies and 'humanity'.
    Then open button 'Sign Up'."""

    logger.info("Visit the Coinbase homepage")

    # Navigate to the main URL (replaces browser.get())
    await page.goto(COINBASE_MAIN_URL)

    # Random sleep
    await asyncio.sleep(random.uniform(1, 3))
    await save_screenshot(text="navigating to 'Home' page", page=page)

    # Simulate mouse movements (Playwright uses page.mouse)
    await page.mouse.move(110, 110)
    await asyncio.sleep(random.uniform(0.6, 1.2))
    await page.mouse.move(70, 150)  # Adjusted to -40, 40 relative movement
    await asyncio.sleep(random.uniform(0.3, 0.9))

    # Click on "Sign Up" (look for the button by CSS selector)
    logger.info("Search button 'Sign Up'")
    signup_button = page.locator('[data-testid="header-get-started-button"]')

    # Wait for the button to be visible and clickable
    await signup_button.wait_for(timeout=SECONDS_TIMEOUT * 1000)  # Convert to ms

    # Simulate mouse movement to button and click
    await signup_button.hover()  # Replaces move_to_element
    await asyncio.sleep(random.uniform(0.5, 1.5))
    await signup_button.click()  # Replaces actions.click()
    logger.info("Clicked 'Sign Up'")
    await asyncio.sleep(random.uniform(1, 3))

    await save_screenshot(text="navigating to 'Sign Up' page", page=page)
