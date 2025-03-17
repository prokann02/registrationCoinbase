import asyncio
import logging
import random

from playwright.async_api import Page, Browser

from config import SECONDS_TIMEOUT
from helpers.save_screenshot import save_screenshot
from pw_functions.click_on_continue_button import click_on_continue_button


async def execute_password_page(browser: Browser, page: Page, user_data):
    """Handle the password entry page."""
    logger = logging.getLogger()

    # Waiting for the password page
    logger.info("Waiting for the password field")
    password_field = page.locator('#confirm-password')
    await password_field.wait_for(timeout=SECONDS_TIMEOUT * 1000)  # Convert to ms

    await password_field.hover()
    await password_field.click()
    await asyncio.sleep(random.uniform(0.5, 1))

    for char in user_data["password"]:
        await password_field.type(char, delay=random.uniform(50, 200))  # Delay in ms

    logger.info("Entered password")
    await save_screenshot(text="entering password", page=page)

    # Close the cookies block if present
    try:
        dismiss_cookies_button = page.locator('[data-testid="dismiss-button"]')
        await dismiss_cookies_button.wait_for(timeout=5_000)  # 5 seconds in ms
        await dismiss_cookies_button.hover()
        await dismiss_cookies_button.click()
        logger.info("Closed cookies block")
        await asyncio.sleep(random.uniform(0.5, 1))
    except Exception:
        logger.info("No cookies block detected")

    # Save the current context to handle potential new tabs
    original_context = page.context

    await click_on_continue_button(page=page)

    # Check if a new tab was opened and ensure focus stays on original
    if len(browser.contexts) > 1 or len(original_context.pages) > 1:
        logger.info("New tab detected after submit, ensuring focus on original page")
        page = original_context.pages[0]  # Switch back to the first page
        await asyncio.sleep(random.uniform(1, 2))
        await click_on_continue_button(page=page)

    await save_screenshot(text="clicking on 'Submit' button in the password page", page=page)

    logger.info("Successfully passed the password entry stage")
