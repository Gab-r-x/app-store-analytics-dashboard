from ..src.tasks.scrape import scrape_categories
from celery.result import AsyncResult
import time

def check_task(task_id):
    """Checks the status of a Celery task."""
    result = AsyncResult(task_id)
    while result.status not in ["SUCCESS", "FAILURE"]:
        print(f"🔄 Waiting for task... Status: {result.status}")
        time.sleep(5)
        result = AsyncResult(task_id)
    
    if result.status == "SUCCESS":
        print(f"✅ Task {task_id} completed successfully!")
    else:
        print(f"❌ Task {task_id} failed! Error: {result.traceback}")
    
    return result.result

# Start the full scraping chain
print("🚀 Starting full scraping pipeline (categories -> apps -> details)...")
task = scrape_categories.delay()
check_task(task.task_id)
print("🎉 All scraping tasks were dispatched successfully!")
