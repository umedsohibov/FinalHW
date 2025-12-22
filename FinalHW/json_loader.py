import requests
import json
import sys

SERVER = "http://localhost:8080"


def load_json_file(filename):
    """Загружает задачи из JSON файла на сервер"""

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            tasks = json.load(f)

        print(f"Найдено {len(tasks)} задач в {filename}")

        created = 0
        for task in tasks:
            resp = requests.post(f"{SERVER}/tasks", json=task)
            if resp.status_code == 201:
                created += 1
                print(f"  ✓ {task['title']}")
            else:
                print(f"  ✗ {task['title']} - ошибка {resp.status_code}")

        print(f"\nИтого создано: {created}/{len(tasks)}")

        # Показываем итог
        resp = requests.get(f"{SERVER}/tasks")
        if resp.status_code == 200:
            all_tasks = resp.json()
            print(f"\nВсего задач на сервере: {len(all_tasks)}")

    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        print("Создайте файл tasks.json с задачами:")
        print('''[
  {"title": "Задача 1", "priority": "high"},
  {"title": "Задача 2", "priority": "normal"}
]''')
    except json.JSONDecodeError:
        print("Ошибка в формате JSON файла")
    except requests.ConnectionError:
        print("Сервер не запущен! Запустите: python todo_server.py")


def create_example_json():
    """Создает пример JSON файла"""
    example = [
        {"title": "Сделать домашку", "priority": "high"},
        {"title": "Купить продукты", "priority": "normal"},
        {"title": "Позвонить другу", "priority": "low"},
        {"title": "Прочитать книгу", "priority": "normal"},
        {"title": "Заплатить за интернет", "priority": "high"}
    ]

    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(example, f, ensure_ascii=False, indent=2)

    print("Создан файл tasks.json с примерами задач")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        load_json_file(sys.argv[1])
    else:
        print("Использование: python json_loader.py [файл.json]")
        print("Или: python json_loader.py --create  (создать пример)")

        # Проверяем есть ли tasks.json
        try:
            with open('tasks.json', 'r'):
                print("\nОбнаружен tasks.json. Загрузить? (y/n): ", end='')
                if input().lower() == 'y':
                    load_json_file('tasks.json')
        except:
            print("\nФайл tasks.json не найден.")
            print("Хотите создать пример? (y/n): ", end='')
            if input().lower() == 'y':
                create_example_json()