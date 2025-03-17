import logging


async def get_input_phone_number():
    logger = logging.getLogger()

    while True:
        phone_number = input("Please write your phone number like: '0960000000': ")
        if not phone_number:
            logger.info("Phone number cannot be empty!")
            continue
        if not phone_number.isdigit():
            logger.info("There should only be numbers!")
            continue
        if len(phone_number) < 7:
            logger.info("The number must contain at least 7 digits!")
            continue
        if len(phone_number) > 15:
            logger.info("The number cannot be longer than 15 digits!")
            continue

        return phone_number
