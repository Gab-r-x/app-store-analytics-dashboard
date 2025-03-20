import os
import time
import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper_categories import get_categories, scrape_top_apps, get_top_lists
from scraper_app_details import get_app_details
from config import MAX_THREADS, TIME_BETWEEN_REQUESTS

# Configurar logging
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_categories():
    logging.info("Iniciando a extração de categorias...")
    categories = get_categories()
    if not categories:
        logging.error("Nenhuma categoria encontrada!")
        return []
    logging.info(f"{len(categories)} categorias encontradas.")
    return categories

def scrape_apps_from_categories(categories):
    """ Obtém os top 100 apps de cada categoria. """
    all_apps = []
    logging.info("Iniciando a extração de aplicativos...")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {}
        for category_name, category_url in categories:
            free_apps_url, paid_apps_url = get_top_lists(category_name, category_url)
            if free_apps_url:
                futures[executor.submit(scrape_top_apps, category_name, "Top Free", free_apps_url)] = category_name
            if paid_apps_url:
                futures[executor.submit(scrape_top_apps, category_name, "Top Paid", paid_apps_url)] = category_name

        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    all_apps.extend(result)
                    logging.info(f"Apps extraídos da categoria {futures[future]}: {len(result)} encontrados.")
            except Exception as e:
                logging.error(f"Erro ao processar categoria {futures[future]}: {e}")

    logging.info(f"Total de {len(all_apps)} aplicativos coletados.")
    return all_apps

def scrape_app_details_parallel(apps):
    all_details = []
    logging.info("Iniciando extração de detalhes dos aplicativos...")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(get_app_details, app[5]): app for app in apps}
        for future in as_completed(futures):
            try:
                details = future.result()
                if details:
                    all_details.append(details)
            except Exception as e:
                logging.error(f"Erro ao obter detalhes do app: {e}")
            time.sleep(TIME_BETWEEN_REQUESTS)
    return all_details

def save_data(apps, app_details):
    os.makedirs("data", exist_ok=True)

    # Salvar apps normalmente
    pd.DataFrame(apps).to_csv("data/top_apps.csv", index=False, sep="|")
    pd.DataFrame(app_details).to_csv("data/app_details.csv", index=False, sep="|")

def main():
    categories = scrape_categories()
    apps = scrape_apps_from_categories(categories)
    app_details = scrape_app_details_parallel(apps)
    save_data(apps, app_details)
    logging.info("✅ Scraping concluído com sucesso!")

if __name__ == "__main__":
    main()
