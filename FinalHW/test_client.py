import requests
import json

SERVER = "http://localhost:8080"


def test_all():
    print("=== ТЕСТИРОВАНИЕ API ===")

    # 1. Создание задачи
    print("\n1. POST /tasks - создание")
    task = {"title": "Тест задача", "priority": "normal"}
    resp = requests.post(f"{SERVER}/tasks", json=task)
    print(f"   Код: {resp.status_code}, Ответ: {resp.json()}")

    # 2. Получение всех задач
    print("\n2. GET /tasks - получение всех")
    resp = requests.get(f"{SERVER}/tasks")
    print(f"   Код: {resp.status_code}")
    print(f"   Задачи: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")

    # 3. Отметка выполнения
    print("\n3. POST /tasks/1/complete - отметка выполнения")
    resp = requests.post(f"{SERVER}/tasks/1/complete")
    print(f"   Код: {resp.status_code}")

    # 4. Проверка изменений
    print("\n4. GET /tasks - проверка изменений")
    resp = requests.get(f"{SERVER}/tasks")
    tasks = resp.json()
    print(f"   Задача выполнена: {tasks[0]['isDone']}")

    print("\n=== ТЕСТ ЗАВЕРШЕН ===")


if __name__ == "__main__":
    test_all()