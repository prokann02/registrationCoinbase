import hashlib
import logging
import time

import requests

from config import SELECTED_AGENT, TEMP_MAIL_API_HOST, TEMP_MAIL_API_URL, LOG_FILE
from helpers.get_proxy import get_selected_proxy

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


async def get_temp_email(email: str, proxy_file, temp_mail_api_key):
    """Receive a temporary email via the temp-mail API."""
    time.sleep(5)
    headers = {
        "User-Agent": SELECTED_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://google.com",
        'x-rapidapi-host': TEMP_MAIL_API_HOST,
        'x-rapidapi-key': temp_mail_api_key,
    }

    email_md5 = hashlib.md5(email.encode()).hexdigest()

    if not proxy_file:
        response = requests.get(f"{TEMP_MAIL_API_URL}/{email_md5}/", headers=headers)
    else:
        selected_proxy = get_selected_proxy()
        response = requests.get(f"{TEMP_MAIL_API_URL}/{email_md5}/", headers=headers,
                                proxies=selected_proxy.get_proxies())

    response.raise_for_status()

    logger.info(f"Success!")
    email_data = response.json()
    email_text = email_data[-1]["mail_text"].replace("Your verification code\n\n", "")
    index = email_text.find("\n\n\n\n")
    email = email_text[:index]
    logger.info(f"Received code: {email}")

    return email
