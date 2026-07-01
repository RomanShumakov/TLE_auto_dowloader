import os
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

# def take_data_from_site():
#     url = "https://www.space-track.org/app/data/whoami"
#     # url = "https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/>now-30/MEAN_MOTION/>11.25/format/3le"
#     api_key = os.getenv('API_KEY')
#     headers = {
#         "apikey": api_key
#     }
#     datas = requests.get(url, headers=headers)
#     # data = requests.get(url, headers=headers, params=params)
#     # data = requests.get(url)
#
#     return datas

def take_data_from_site():
    load_dotenv()
    identity = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    credentials = {
        'identity': identity,
        'password': password
    }

    # Создаем сессию
    session = requests.Session()

    # 1. Сначала логинимся
    login_url = 'https://www.space-track.org/ajaxauth/login'
    response = session.post(login_url, data=credentials)

    # Проверяем, что логин прошел успешно (должен быть код 200)
    if response.status_code != 200:
        print("Не удалось залогиниться, проверь почту, пароль и VPN.")
    else:
        print("Авторизация прошла успешно!")
        authorisation_data = session.get("https://www.space-track.org/app/data/whoami")

        authorisation = authorisation_data.json()
        print(f'Пользователь: {authorisation["identity"]} Активность: {authorisation["logged_in"]}')


        # 2. Теперь делаем сам запрос за данными (например, TLE)
        # работающий юрл:
        # query_url = 'https://www.space-track.org/basicspacedata/query/class/satcat/limit/1/format/json'
        query_url = 'https://www.space-track.org/basicspacedata/query/class/gp/orderby/EPOCH%20desc/format/json'
        data_response = session.get(query_url)

        if data_response.status_code != 200:
            print(f"Не удалось получить данные. Код ошибки: {data_response.status_code}")
        else:
            return data_response.json()


def data_writer(data):
    today = datetime.now().strftime("%Y-%m-%d")

    folderpath = os.path.join("TLE", today)

    os.makedirs(folderpath, exist_ok=True)
    file_path = os.path.join(folderpath, 'ALL.txt')

        # Открываем файл satellites.txt в режиме записи ('w')
    with open(file_path , 'w', encoding='utf-8') as file:
        for entry in data:
            name = entry.get('OBJECT_NAME', 'Unknown')
            tle_line1 = entry.get('TLE_LINE1')
            tle_line2 = entry.get('TLE_LINE2')

            file.write(f"{name}\n{tle_line1}\n{tle_line2}\n")

    print(f"Готово! Записано {len(data)} объектов в файл ALL.txt")



if __name__ == "__main__":
    res_data = take_data_from_site()
    data_writer(res_data)