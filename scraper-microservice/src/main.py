from tasks.scrape import scrape_categories, scrape_apps_from_categories, scrape_app_details_parallel

def main():
    """Runs the scraping pipeline."""
    categories = scrape_categories.delay()
    apps = scrape_apps_from_categories.delay(categories.get())
    app_details = scrape_app_details_parallel.delay(apps.get())

if __name__ == "__main__":
    main()