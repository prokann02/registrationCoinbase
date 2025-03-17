import asyncio
import logging
import os
import random
import time

from config import LOG_DIR, TEMP_MAIL_API_DOMAINS
from helpers.generate_user_data import generate_user_data
from helpers.get_input_phone_number import get_input_phone_number
from helpers.get_proxy import get_proxy
from helpers.init_args import init_args
from pw_functions.register_on_coinbase import pw_run

# Logging setup
log_file = os.path.join(LOG_DIR, "program.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


async def main():
    # german
    # +4915123456789
    # singapore
    # +6581234567
    # france
    # +33612345678
    args = await init_args()
    phone = args.phone_number
    temp_mail_api_key = args.temp_mail_api_key
    captcha_api_key = args.captcha_api_key
    proxy_file = args.proxy_file

    if not phone:
        phone = await get_input_phone_number()

    if proxy_file:
        await get_proxy(proxy_file=proxy_file)

    user_data = await generate_user_data(
        phone_number=phone,
    )

    unique_value = round(time.thread_time(), 3)
    email = (f"{user_data['first_name'].lower()}__{user_data['last_name'].lower()}{unique_value}"
             f"{random.choice(TEMP_MAIL_API_DOMAINS)}")

    await pw_run(
        proxy_file=proxy_file,
        user_data=user_data,
        email=email,
        temp_mail_api_key=temp_mail_api_key,
        captcha_api_key=captcha_api_key,
    )


if __name__ == "__main__":
    asyncio.run(main())
