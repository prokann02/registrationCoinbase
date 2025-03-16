import logging
import time

from config import LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


async def save_screenshot(text, page):
    """Save the screenshot after entering the code"""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshots/screenshot_{text.replace(' ', '_')}_{timestamp}.png"
    await page.screenshot(path=filename)
    logger.info(f"Saved screenshot after {text}")
