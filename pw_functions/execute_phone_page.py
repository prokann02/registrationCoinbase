import asyncio
import logging
import random

from playwright.async_api import Page

from config import SECONDS_TIMEOUT
from helpers.save_screenshot import save_screenshot
from pw_functions.click_on_continue_button import click_on_continue_button
from pw_functions.solve_captcha import solve_captcha


async def execute_phone_page(page: Page, phone_number: str, country_code: str, captcha_api_key: str):
    """Fill the phone page with country code and number."""
    logger = logging.getLogger()

    # Wait for the phone page to load
    logger.info("Waiting for phone page to load")
    dropdown = page.locator('[data-testid="country-select-searchable"]')
    await dropdown.wait_for(timeout=SECONDS_TIMEOUT * 1000)

    # Click the dropdown to open it
    logger.info(f"Opening country code dropdown to select {country_code}")
    await dropdown.hover()
    await dropdown.click()
    await asyncio.sleep(random.uniform(1, 2))

    # Find the search input field and enter the country code
    search_input = page.locator("xpath=//input[@aria-label='Search']")
    await search_input.wait_for(timeout=20_000)
    await search_input.hover()
    await search_input.click()
    await asyncio.sleep(random.uniform(0.5, 1))
    await search_input.fill("")  # Clear the field
    for char in country_code:
        await search_input.type(char, delay=random.uniform(100, 200))
    logger.info(f"Entered country code '{country_code}' into search field")

    # Select the first button that contains the country code
    country_button = page.locator(f"xpath=//button[contains(@aria-label, '{country_code}')]")
    await country_button.wait_for(timeout=20_000)
    await country_button.hover()
    await country_button.click()
    logger.info(f"Selected country code: {country_code}")

    # Find and fill the phone number input field
    phone_field = page.locator('[data-testid="phone-number"]')
    await phone_field.wait_for(timeout=20_000)
    await phone_field.hover()
    await phone_field.click()
    await asyncio.sleep(random.uniform(1, 2))
    for char in phone_number:
        await phone_field.type(char, delay=random.uniform(100, 250))
    logger.info("Entered phone number")

    await click_on_continue_button(page=page)
    await save_screenshot(text="entering phone page", page=page)

    if await solve_captcha(page=page, captcha_api_key=captcha_api_key):
        logger.info("Captcha after entering phone solved")

    await asyncio.sleep(random.uniform(1, 2))
    logger.info("All finished!")
    await asyncio.sleep(30)