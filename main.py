import os
from datetime import datetime
from dotenv import load_dotenv
import requests


def get_session():
    """Создает авторизованную сессию"""
    load_dotenv()
    identity = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    session = requests.Session()
    login_url = 'https://www.space-track.org/ajaxauth/login'

    try:
        response = session.post(login_url, data={'identity': identity, 'password': password})
        if response.status_code == 200:
            print("Авторизация прошла успешно!")
            authorisation_data = session.get("https://www.space-track.org/app/data/whoami")

            authorisation = authorisation_data.json()
            print(f'Пользователь: {authorisation["identity"]} Активность: {authorisation["logged_in"]}')
            return session
        else:
            print("Ошибка авторизации.")
            return None
    except Exception as e:
        print(f"Ошибка при попытке входа: {e}")
        return None

def fetch_data(session, url):
    """Качает данные по конкретной ссылке"""
    try:
        response = session.get(url)
        if response.status_code == 200:
            return response.json()
        print(f"Ошибка запроса: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при скачивании: {e}")
    return None


def data_writer(data, filename_prefix):
    """Сохраняет данные в файл с нужным именем"""

    if not data:
        print("Данных нет, записывать нечего.")
        return None

    today = datetime.now().strftime("%Y%m%d")
    folderpath = os.path.join("TLE", today)
    os.makedirs(folderpath, exist_ok=True)
    file_path = os.path.join(folderpath, f'{filename_prefix}.txt')

    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            name = entry.get('OBJECT_NAME', 'Unknown')
            tle_line1 = entry.get('TLE_LINE1')
            tle_line2 = entry.get('TLE_LINE2')

            file.write(f"{name}\n{tle_line1}\n{tle_line2}\n")

    print(f"Файл {filename_prefix}.txt оформлен. Записано объектов: {len(data)}. Суммарно строк: {len(data) * 3}")


if __name__ == "__main__":

    CONFIGS  = {
        "ALL": "https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/%3Enow-30/orderby/NORAD_CAT_ID,EPOCH/format/json",
        "LEO": "https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/%3Enow-30/MEAN_MOTION/%3E11.25/ECCENTRICITY/%3C0.25/OBJECT_TYPE/payload/orderby/NORAD_CAT_ID,EPOCH/format/json"
    }
    active_session = get_session()

    if active_session:
        for name, url in CONFIGS.items():
            print(f"\nРаботаю с категорией спутников: {name}...")
            downloaded_data = fetch_data(active_session, url)
            data_writer(downloaded_data, name)

        print("\nВсе задачи выполнены!")

