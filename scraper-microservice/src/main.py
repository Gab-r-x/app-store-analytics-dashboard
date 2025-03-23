import time
import socket
from tasks.scrape import scrape_categories

def wait_for_rabbitmq(host='rabbitmq', port=5672, timeout=30):
    """Waits for RabbitMQ to be available before starting tasks."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                print("✅ RabbitMQ is available!")
                return
        except OSError:
            print("⏳ Waiting for RabbitMQ...")
            time.sleep(2)
    raise TimeoutError("❌ RabbitMQ not available after waiting.")

def main():
    wait_for_rabbitmq()
    scrape_categories.delay()

if __name__ == "__main__":
    main()
