import random

# Número máximo de threads para scraping paralelo
MAX_THREADS = 8

MAX_RETRIES = 3

# Tempo de espera entre requisições (segundos)
TIME_BETWEEN_REQUESTS = random.uniform(1, 3)

# Lista de User-Agents para evitar bloqueios
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
]

# URL base da App Store
BASE_URL = "https://apps.apple.com"
