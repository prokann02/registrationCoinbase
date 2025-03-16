import itertools
import os
import random

# CAPTCHA SETTINGS
CAPTCHA_URL = "https://2captcha.com/uk/enterpage"

# TEMP MAIL SETTINGS
TEMP_MAIL_API_URL = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id"
TEMP_MAIL_API_HOST = "privatix-temp-mail-v1.p.rapidapi.com"
TEMP_MAIL_API_DOMAINS = ["@cevipsa.com", "@cpav3.com", "@nuclene.com", "@steveix.com", "@mocvn.com",
                         "@tenvil.com", "@tgvis.com", "@amozix.com", "@anypsd.com", "@maxric.com", ]

# USER AGENT SETTINGS
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; Pixel C Build/OPR1.170623.027) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 OPR/77.0.4054.172 Safari/537.36",
]
# Randomly get one user agent from list
SELECTED_AGENT = random.choice(USER_AGENTS) if USER_AGENTS else None

# REGISTRATION SETTINGS
FIRST_NAMES = ["John", "Emma", "Liam", "Olivia", "Noah", "Ava", "James", "Sophia", "William", "Isabella"]
LAST_NAMES = ["Smith", "Johnson", "Brown", "Taylor", "Wilson", "Davis", "Clark", "Lewis", "Walker", "Hall"]

# COINBASE SETTINGS
COINBASE_MAIN_URL = "https://www.coinbase.com"
COINBASE_LOGIN_URL = "http://login.coinbase.com/signup"

# FOLDER SETTINGS
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "program.log")

# Folder for screenshots
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# PLAYWRIGHT SETTINGS
SECONDS_TIMEOUT = 40
