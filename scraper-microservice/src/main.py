from tasks.scrape import scrape_categories
import os

def main():
    celery_broker = os.getenv("CELERY_BROKER_URL", "")
    if "cloudamqp" in celery_broker:
        print("✅ Skipping RabbitMQ wait (using CloudAMQP broker)")
    else:
        print("⚠️ CELERY_BROKER_URL não parece ser CloudAMQP, verifique.")
    scrape_categories.delay()

if __name__ == "__main__":
    main()
