import asyncio
import logging
import sys

from playwright.async_api import Page
from twocaptcha import TwoCaptcha

from config import LOG_FILE
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


async def solve_captcha(page: Page, captcha_api_key: str, max_attempts=4):
    """
    Detects and solves various types of captchas via 2Captcha, looping until no captchas remain.
    Returns True if all captchas are solved, False if unsolved after max_attempts.
    """
    attempt = 0
    captcha_solved = False

    while attempt < max_attempts:
        attempt += 1
        logger.info(f"Captcha solving attempt {attempt}/{max_attempts}")

        try:
            # No need to switch to default content in Playwright; operates on page directly

            # Check for Arkose Labs/FunCAPTCHA
            if await solve_arkose_captcha(page=page, captcha_api_key=captcha_api_key):
                captcha_solved = True
                await save_screenshot(text="solving Captcha!", page=page)

                # Check if another captcha appears after solving
                await asyncio.sleep(2)  # Wait for page to update
                if not await is_captcha_present(page=page):
                    logger.info("All Arkose captchas resolved")
                    return True
                logger.info("Arkose captcha solved, but another detected")

            else:
                logger.info("No recognizable captcha found on this attempt")
                if not captcha_solved:
                    logger.info("No captchas detected initially, assuming none present")
                    return True
                break  # Exit if no more captchas detected after solving one

        except Exception as e:
            logger.error(f"Error during captcha solving attempt {attempt}: {e}")
            await asyncio.sleep(1)  # Brief pause before retry

    logger.warning(f"Failed to resolve all captchas after {max_attempts} attempts")
    return False


async def is_captcha_present(page: Page) -> bool:
    """Check if any captcha iframe is still present on the page."""
    try:
        captcha_iframe = page.locator(
            "xpath=//iframe[contains(@src, 'arkoselabs') or contains(@src, 'recaptcha') or contains(@src, 'hcaptcha')]"
        )
        await captcha_iframe.wait_for(timeout=3_000)
        return True
    except Exception:
        return False


async def solve_arkose_captcha(page: Page, captcha_api_key: str) -> bool | None:
    """Solve Arkose Labs/FunCAPTCHA."""
    try:
        # Locate the outer iframe
        recaptcha_iframe = page.locator("xpath=//div/iframe")
        await recaptcha_iframe.wait_for(timeout=5_000)
        iframe_element = await recaptcha_iframe.element_handle()
        iframe_page = await iframe_element.content_frame()
        logger.info("Arkose Labs captcha iframe found")

        # Locate the inner iframe within the first iframe
        recaptcha_iframe2 = iframe_page.locator("xpath=//iframe")
        await recaptcha_iframe2.wait_for(timeout=5_000)
        iframe2_element = await recaptcha_iframe2.element_handle()
        inner_iframe_page = await iframe2_element.content_frame()

        try:
            # Click the "Start Puzzle" button
            button = inner_iframe_page.locator("xpath=//button[contains(text(), 'Start Puzzle')]")
            await button.wait_for(timeout=5_000)
            await button.click()
        except Exception as e:
            logger.info("'Start puzzle' not found, skipping...")

        sitekey = None
        sitekey_locator = page.locator("xpath=//*[@data-sitekey and string-length(@data-sitekey) > 0]")
        sitekey_elements = await sitekey_locator.all()  # Get all matching elements
        if sitekey_elements:
            # Take the first element with a non-empty data-sitekey
            for element in sitekey_elements:
                potential_sitekey = await element.get_attribute("data-sitekey")
                if potential_sitekey and potential_sitekey.strip():  # Ensure it’s not empty
                    sitekey = potential_sitekey
                    break

        if not sitekey:
            script_locator = page.locator("xpath=//script[contains(@src, 'arkoselabs')]")
            src = await script_locator.get_attribute("src")
            sitekey = src.split('/')[-2] if src else None

        if not sitekey:
            logger.error("Could not find a valid sitekey for Arkose Labs CAPTCHA")
            return False

        url = page.url

        # Solve via 2Captcha
        solver = TwoCaptcha(captcha_api_key)
        try:
            result = await asyncio.to_thread(solver.funcaptcha, sitekey=sitekey, url=url)
        except Exception:
            try:
                result = await asyncio.to_thread(solver.funcaptcha, sitekey=sitekey, url=url)
            except Exception as e:
                logger.warning(f"TwoCaptcha can't solve CAPTCHA!!!\n{e}\nExit!")
                sys.exit(1)

        captcha_code = result['code']
        logger.info(f"Arkose captcha solved: {captcha_code}")

        # Inject the token into the iframe
        await iframe_page.evaluate(f"""
            console.log('Injecting token: {{arguments[0]}}');

            // Try common hidden fields
            var fields = ['fc-token', 'session_token', 'verification-token', 'arkose_token'];
            fields.forEach(function(id) {{
                var el = document.getElementById(id);
                if (el) {{
                    el.value = '{{arguments[0]}}';
                    console.log('Set token in ' + id);
                }}
            }});

            // Try common callbacks
            var callbacks = ['arkoseCallback', 'onCompleted', 'onCaptchaSuccess', 'callback'];
            callbacks.forEach(function(cb) {{
                if (window[cb]) {{
                    window[cb]('{{arguments[0]}}');
                    console.log('Called ' + cb);
                }}
            }});

            // Log available window properties for debugging
            var props = Object.keys(window).filter(p => p.toLowerCase().includes('arkose') || p.toLowerCase().includes('captcha'));
            console.log('Possible captcha-related properties:', props);
        """, captcha_code)

        await asyncio.sleep(5)
        submit_button = inner_iframe_page.locator("xpath=//button[contains(text(), 'Submit')]")

        try:
            await submit_button.wait_for(timeout=5_000)
            await submit_button.click()
            logger.info("Clicked submit button")
            return True
        except Exception as e:
            logger.info(f"{e}")

    except Exception as e:
        logger.info(f"No Arkose Labs captcha detected or error: {e}")
        return False
