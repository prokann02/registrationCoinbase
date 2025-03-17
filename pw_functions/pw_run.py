from playwright.async_api import async_playwright

from pw_functions.register_on_coinbase import register_on_coinbase
from pw_functions.start_browser import start_browser


async def pw_run(proxy_file, user_data, email, temp_mail_api_key, captcha_api_key):
    async with async_playwright() as playwright:
        browser, page = await start_browser(playwright, proxy_file=proxy_file)

        await register_on_coinbase(
            browser=browser,
            user_data=user_data,
            email=email,
            page=page,
            proxy_file=proxy_file,
            temp_mail_api_key=temp_mail_api_key,
            captcha_api_key=captcha_api_key,
        )

        await browser.close()
