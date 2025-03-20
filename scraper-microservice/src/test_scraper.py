from tasks.scrape import scrape_categories, scrape_apps_from_categories, scrape_app_details_parallel
from celery.result import AsyncResult
from pymongo import MongoClient
import time

def check_task(task_id):
    """Verifica o status de uma tarefa Celery."""
    result = AsyncResult(task_id)
    while result.status not in ["SUCCESS", "FAILURE"]:
        print(f"🔄 Aguardando conclusão... Status: {result.status}")
        time.sleep(5)  # Espera 5s antes de verificar de novo
        result = AsyncResult(task_id)
    
    if result.status == "SUCCESS":
        print(f"✅ Task {task_id} finalizada com sucesso!")
    else:
        print(f"❌ Task {task_id} falhou! Erro: {result.traceback}")
    
    return result.result

# 1️⃣ Executa a tarefa de scraping das categorias
print("🚀 Iniciando scraping das categorias...")
task_1 = scrape_categories.delay()
categories = check_task(task_1.task_id)

if not categories:
    print("❌ Nenhuma categoria encontrada. Abortando.")
    exit()

# 2️⃣ Executa a tarefa de scraping dos apps das categorias
print("🚀 Iniciando scraping dos apps das categorias...")
task_2 = scrape_apps_from_categories.delay(categories)
apps = check_task(task_2.task_id)

if not apps:
    print("❌ Nenhum app encontrado. Abortando.")
    exit()

# 3️⃣ Conectar ao MongoDB para buscar os apps salvos
client = MongoClient("mongodb://mongo:27017/")
db = client["scraper_data"]

# Buscar os primeiros 10 apps salvos no banco, removendo _id
apps_list = list(db.raw_apps.find({}, {"_id": 0, "url": 1}))

if not apps_list:
    print("❌ Nenhum app encontrado no banco. Abortando.")
    exit()

# 4️⃣ Executa a tarefa de scraping dos detalhes dos apps
print("🚀 Iniciando scraping dos detalhes dos apps...")
task_3 = scrape_app_details_parallel.delay(apps_list)
check_task(task_3.task_id)

print("🎉 Todas as tarefas foram concluídas com sucesso!")
