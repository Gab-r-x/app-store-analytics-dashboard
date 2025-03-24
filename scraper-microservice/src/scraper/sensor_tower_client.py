import requests
import logging
import random
from bs4 import BeautifulSoup
from config import settings

USER_AGENTS = settings.USER_AGENTS

# Logging
logger = logging.getLogger(__name__)

LOGIN_URL = "https://app.sensortower.com/users/sign_in?product=st"


def get_authenticity_token(session: requests.Session) -> str:
    """Fetch the authenticity_token required for login."""
    response = session.get(LOGIN_URL)
    if response.status_code != 200:
        logger.error("❌ Failed to fetch login page for authenticity token")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    token_input = soup.find("input", {"name": "authenticity_token"})
    return token_input["value"] if token_input else ""


def login_to_sensortower() -> requests.Session:
    """Logs into Sensor Tower and returns an authenticated session."""
    session = requests.Session()
    token = get_authenticity_token(session)

    if not token:
        logger.error("❌ Could not extract authenticity_token")
        return None

    payload = {
        "utf8": "✓",
        "authenticity_token": token,
        "user[email]": settings.SENSORTOWER_LOGIN,
        "user[password]": settings.SENSORTOWER_PASS,
        "user[otp_attempt]": ""
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": LOGIN_URL,
        "Origin": "https://app.sensortower.com"
    }

    response = session.post(LOGIN_URL, headers=headers, data=payload, allow_redirects=True)

    if response.status_code in [200, 302]:
        logger.info("✅ Successfully logged in to Sensor Tower")
        return session
    else:
        logger.error(f"❌ Login failed with status {response.status_code}")
        return None
