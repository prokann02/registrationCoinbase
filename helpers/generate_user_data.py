import logging
import random
import string

import phonenumbers

from config import FIRST_NAMES, LAST_NAMES
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


async def generate_random_password(length=8):
    """Generates a random password of the specified length."""
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length)) + '?5gT'
    return password


async def get_phone_code_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country_code = parsed_number.country_code
        return f"+{country_code}", str(parsed_number.national_number)

    except phonenumbers.NumberParseException:
        return "Invalid number format"


async def generate_user_data(phone_number):
    """Generates user data: first name, last name, password and returns them along with the phone number."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    password = await generate_random_password()

    phone_code, phone_number = await get_phone_code_number(phone_number=phone_number)

    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "phone_number": phone_number,
        "phone_code": phone_code,
    }

    logger.info(f"Generated data: {user_data}")

    return user_data
