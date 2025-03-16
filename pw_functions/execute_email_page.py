import asyncio
import logging
import random

from playwright.async_api import Browser, Page

from config import LOG_FILE, SECONDS_TIMEOUT
from helpers.save_screenshot import save_screenshot
from pw_functions.click_on_continue_button import click_on_continue_button

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


async def execute_email_page(email: str, page: Page):
    """Enter the email on the registration page."""
    logger.info("Enter email")

    # Locate the email field
    email_field = page.locator('[data-testid="email"]')
    await email_field.wait_for(timeout=SECONDS_TIMEOUT * 1000)  # Convert to ms

    # Simulate mouse movement to the field and click
    await email_field.hover()
    await email_field.click()
    await asyncio.sleep(random.uniform(0.5, 1))

    # Type email character by character
    for char in email:
        await email_field.type(char, delay=random.uniform(50, 200))  # Delay in ms

    await click_on_continue_button(page=page)  # Updated to use page
    await save_screenshot(text="clicking on 'Continue' button in the first page", page=page)
