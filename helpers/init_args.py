import argparse
import os

from dotenv import load_dotenv


async def init_args():
    load_dotenv()

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--captcha-api-key',
                        help='API key for 2Captcha (https://2captcha.com/uk/enterpage)',
                        default=os.getenv('CAPTCHA_API_KEY'))

    parser.add_argument('-m', '--temp-mail-api-key',
                        help='API key for Temp Mail (https://temp-mail.org/uk/api)',
                        default=os.getenv('TEMP_MAIL_API_KEY'))

    parser.add_argument('-n', '--phone-number', help='Full phone number with code', required=False)

    parser.add_argument('-f', '--proxy-file', help='TXT file with proxies', required=False)

    args = parser.parse_args()

    if not args.captcha_api_key or not args.temp_mail_api_key:
        parser.error(
            "Both CAPTCHA and Temp Mail API keys are required. Provide them via .env or command-line arguments.")

    return args
