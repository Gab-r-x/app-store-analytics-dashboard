from tasks.process_data import celery_app

if __name__ == "__main__":
    celery_app.start()
