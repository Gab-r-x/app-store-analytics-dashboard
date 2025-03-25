import logging
import random
import time
from config import settings
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_AGENTS = settings.USER_AGENTS
LOGIN_URL = "https://app.sensortower.com/users/sign_in?product=st"

logger = logging.getLogger(__name__)


def create_driver() -> uc.Chrome:
    user_agent = random.choice(USER_AGENTS)
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")

    logger.info(f"🧠 Using User-Agent: {user_agent}")

    driver = uc.Chrome(options=options)
    return driver

def login_with_selenium() -> uc.Chrome:
    driver = create_driver()
    driver.get(LOGIN_URL)

    try:
        # 1. Preenche e envia o e-mail
        email_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "user[email]"))
        )
        email_input.send_keys(settings.SENSORTOWER_LOGIN)
        email_input.send_keys(Keys.RETURN)

        logger.info("📧 Email enviado. Aguardando campo de senha...")

        # 2. Espera o campo de senha aparecer e envia a senha
        password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "user[password]"))
        )
        password_input.send_keys(settings.SENSORTOWER_PASS)
        password_input.send_keys(Keys.RETURN)

        logger.info("🔐 Senha enviada. Aguardando redirecionamento...")

        # 3. Aguarda redirecionamento após login
        WebDriverWait(driver, 15).until(
            EC.url_contains("/overview")
        )

        logger.info("✅ Login completo com sucesso!")
        return driver

    except Exception as e:
        logger.error(f"❌ Error durante o login em duas etapas: {e}")
        driver.quit()
        return None
