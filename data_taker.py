import os
from datetime import datetime
from dotenv import load_dotenv
import requests


def take_data_from_site():
    load_dotenv()
    identity = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    credentials = {
        'identity': identity,
        'password': password
    }

    session = requests.Session()

    login_url = 'https://www.space-track.org/ajaxauth/login'

    try:
        response = session.post(login_url, data=credentials)

        if response.status_code != 200:
            print("Не удалось зарегистрироваться в системе. Проверьте почту, пароль, и соединение (VPN).")
        else:
            print("Авторизация прошла успешно!")
            authorisation_data = session.get("https://www.space-track.org/app/data/whoami")

            authorisation = authorisation_data.json()
            print(f'Пользователь: {authorisation["identity"]} Активность: {authorisation["logged_in"]}')
            print("Выполняю скачивание базы TLE...")

            try:
                query_url = 'https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/%3Enow-30/orderby/NORAD_CAT_ID,EPOCH/format/json'

                data_response = session.get(query_url)

                if data_response.status_code != 200:
                    print(f"Не удалось получить данные. Код ошибки: {data_response.status_code}")
                    return None
                else:
                    return data_response.json()
            except Exception as e:
                print(f"Что-то пошло не так: {e}")
                return None

    except Exception as e:
        print(f"Что-то пошло не так: {e}")
        return None


def data_writer(data):
    if not data:
        print("Данных нет, записывать нечего.")
        return None

    today = datetime.now().strftime("%Y%m%d")

    folderpath = os.path.join("TLE", today)

    os.makedirs(folderpath, exist_ok=True)
    file_path = os.path.join(folderpath, 'ALL.txt')

    lines_count = 0
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            name = entry.get('OBJECT_NAME', 'Unknown')
            tle_line1 = entry.get('TLE_LINE1')
            tle_line2 = entry.get('TLE_LINE2')
            lines_count += 3

            file.write(f"{name}\n{tle_line1}\n{tle_line2}\n")

    print(f"Готово! Записано {len(data)} объектов в файл ALL.txt")
    if lines_count == len(data) * 3:
        print(f"Общая проверка целостности пройдена: записано {lines_count} строк.")
    else:
        print(f"Ошибка целостности! Ожидалось {len(data) * 3}, но записано {lines_count}.")


if __name__ == "__main__":
    downloaded_data = take_data_from_site()
    data_writer(downloaded_data)
