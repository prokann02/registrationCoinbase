import logging
import random
import sys

from playwright.async_api import Page, Browser

from config import SECONDS_TIMEOUT
from helpers.get_proxy import search_oops_page
from helpers.get_temp_email import get_temp_email
from helpers.save_screenshot import save_screenshot
from pw_functions.execute_email_page import execute_email_page
from pw_functions.execute_home_page_and_open_login import execute_home_page_and_open_login
from pw_functions.execute_name_page import execute_name_page
from pw_functions.execute_password_page import execute_password_page
from pw_functions.execute_phone_page import execute_phone_page
from pw_functions.pw_run import pw_run
from pw_functions.search_person_script import search_person_script
from pw_functions.search_welcome_script import search_welcome_script


async def register_on_coinbase(browser: Browser, user_data, email, page: Page, proxy_file, temp_mail_api_key,
                               captcha_api_key):
    """Register on Coinbase using generated data and temporary email."""
    logger = logging.getLogger()

    try:
        await execute_home_page_and_open_login(page=page)

        await search_welcome_script(page=page)

        if await search_oops_page(page=page, browser=browser):
            await pw_run(proxy_file, user_data, email, temp_mail_api_key, captcha_api_key)
            return

        await execute_email_page(
            email=email,
            page=page,
        )

        await search_person_script(page=page)

        if await search_oops_page(page=page, browser=browser):
            await pw_run(proxy_file, user_data, email, temp_mail_api_key, captcha_api_key)
            return

        # Wait for the transition to the code entry stage
        code_container = page.locator('[data-testid="code-inputs-container"]')
        await code_container.wait_for(timeout=SECONDS_TIMEOUT * 1000)  # Convert to ms
        logger.info("We have moved on to the code entry stage.")

        # Get verification code (assuming get_temp_email is defined elsewhere)
        verification_code = await get_temp_email(
            email=email,
            proxy_file=proxy_file,
            temp_mail_api_key=temp_mail_api_key,
        )

        # Locate the code input container
        code_input_container = page.locator('[data-testid="piroka"]')
        await code_input_container.wait_for(timeout=SECONDS_TIMEOUT * 1000)  # Convert to ms

        # Find all input elements within the container
        code_inputs = await code_input_container.locator("css=input").all()
        if len(code_inputs) != 6:
            logger.error(f"Incorrect number of fields for entering the code: {len(code_inputs)}")
            sys.exit(1)

        # Enter the code character by character
        logger.info("Enter the confirmation code")
        for i, digit in enumerate(verification_code):
            await code_inputs[i].type(digit, delay=random.uniform(100, 300))  # Delay in ms

        await save_screenshot(text="entering the code in the second page", page=page)

        if await search_oops_page(page=page, browser=browser):
            await pw_run(proxy_file, user_data, email, temp_mail_api_key, captcha_api_key)
            return

        await execute_password_page(
            user_data=user_data,
            browser=browser,
            page=page,
        )

        await execute_name_page(page=page, user_data=user_data)

        await execute_phone_page(
            page=page,
            phone_number=user_data['phone_number'],
            country_code=user_data['phone_code'],
            captcha_api_key=captcha_api_key,
        )

        await save_screenshot(text="ending all actings", page=page)

    except Exception as e:
        logger.error(f"Registration error: {e}")
        await save_screenshot(page=page, text="error in register_on_coinbase()")
        await browser.close()
        raise
