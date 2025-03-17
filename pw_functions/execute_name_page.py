import asyncio
import logging
import random

from playwright.async_api import Page

from config import SECONDS_TIMEOUT
from helpers.save_screenshot import save_screenshot
from pw_functions.click_on_continue_button import click_on_continue_button


async def execute_name_page(page: Page, user_data):
    """Fill out the page with the first and last name."""
    logger = logging.getLogger()

    logger.info("Fill out the page with the first and last name")

    # Field for first name
    first_name_field = page.locator('[data-testid="display-name-first-name-input"]')
    await first_name_field.wait_for(timeout=SECONDS_TIMEOUT * 1000)  # Convert to ms
    await first_name_field.hover()
    await first_name_field.click()
    await asyncio.sleep(random.uniform(0.5, 1))
    for char in user_data["first_name"]:
        await first_name_field.type(char, delay=random.uniform(50, 200))  # Delay in ms
    logger.info("Entered first name")

    # Field for last name
    last_name_field = page.locator('[data-testid="display-name-last-name-input"]')
    await last_name_field.wait_for(timeout=20_000)  # 20 seconds in ms
    await last_name_field.hover()
    await last_name_field.click()
    await asyncio.sleep(random.uniform(0.5, 1))
    for char in user_data["last_name"]:
        await last_name_field.type(char, delay=random.uniform(50, 200))  # Delay in ms
    logger.info("Entered last name")

    await click_on_continue_button(page=page)
    await save_screenshot(text="name_page", page=page)
