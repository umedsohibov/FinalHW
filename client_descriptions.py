import csv
from typing import List, Dict


def load_csv(file_path: str) -> List[Dict[str, str]]:
    """грузим данные .csv в список словарей"""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
    except Exception as e:
        print(f"Ошибка при загрузке CSV: {e}")
    return data


def format_gender(gender: str) -> str:
    """переводим пол в юзабельный вид"""
    gender_map = {
        'female': 'женского',
        'male': 'мужского'
    }
    return gender_map.get(gender.lower(), gender)


def format_device(device: str) -> str:
    """переводим устройство"""
    device_map = {
        'mobile': 'мобильного',
        'desktop': 'десктопного',
        'laptop': 'ноутбука',
        'tablet': 'планшета'
    }
    return device_map.get(device.lower(), device)


def format_browser(browser: str) -> str:
    return browser


def format_region(region: str) -> str:
    """Форматирует регион (если тире меняем 'не указан')"""
    if region == '-' or not region.strip():
        return 'не указан'
    return region


def generate_description(client: Dict[str, str]) -> str:
    """Генерирует текстовое описание для одного клиента"""
    name = client.get('name', 'Неизвестный')
    gender = format_gender(client.get('sex', ''))
    age = client.get('age', 'Неизвестно')
    device = format_device(client.get('device_type', ''))
    browser = format_browser(client.get('browser', ''))
    bill = client.get('bill', '0')
    region = format_region(client.get('region', ''))

    # Определяем правильную форму глагола
    if client.get('sex', '').lower() == 'female':
        verb = 'совершила'
    else:
        verb = 'совершил'

    description = (
        f"Пользователь {name} {gender} пола, {age} лет {verb} покупку на "
        f"{bill} у.е. с {device} браузера {browser}. "
        f"Регион, из которого совершалась покупка: {region}.\n"
    )
    return description


def generate_all_descriptions(data: List[Dict[str, str]]) -> List[str]:
    """Генерирует описания для всех клиентов"""
    descriptions = []
    for client in data:
        description = generate_description(client)
        descriptions.append(description)
    return descriptions


def save_to_txt(descriptions: List[str], output_file: str) -> None:
    """Сохраняет описания в TXT-файл"""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for i, description in enumerate(descriptions, 1):
                file.write(f"{i}. {description}")
        print(f"Описания сохранены в файл: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")


def main():
    """Основная функция программы"""
    input_file = '.venv/HW7/web_clients_correct-старое.csv'
    output_file = 'client_descriptions.txt'

    # 1. Загружаем CSV-файл
    data = load_csv(input_file)

    if not data:
        print("Не удалось загрузить данные или файл пуст")
        return

    print(f"Загружено {len(data)} записей из CSV-файла")

    # 2. Генерируем описания
    descriptions = generate_all_descriptions(data)

    # 3. Сохраняем в TXT-файл
    save_to_txt(descriptions, output_file)


if __name__ == "__main__":
    main()