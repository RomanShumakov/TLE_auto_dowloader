import os
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
        print("Не удалось залогиниться, проверь почту и пароль.")
    else:
        print("Авторизация прошла успешно!")
        authorisation_data = session.get("https://www.space-track.org/app/data/whoami")

        authorisation = authorisation_data.json()
        print(f'Пользователь: {authorisation["identity"]} Активность: {authorisation["logged_in"]}')


        # 2. Теперь делаем сам запрос за данными (например, TLE)
        # работающий юрл:
        # query_url = 'https://www.space-track.org/basicspacedata/query/class/satcat/limit/1/format/json'
        query_url = 'https://www.space-track.org/basicspacedata/query/class/gp/orderby/EPOCH%20desc/limit/5/format/json'



        data_response = session.get(query_url)

        if data_response.status_code != 200:
            print(f"Ошибка. Не удалось получить данные. Код {data_response.status_code}")
        else:
            tles = data_response.json()
            for entry in tles:
                # Достаем название спутника и саму TLE-строку
                name = entry.get('OBJECT_NAME', 'Unknown')
                tle_line1 = entry.get('TLE_LINE1')
                tle_line2 = entry.get('TLE_LINE2')
                print(f"Спутник: {name}\n{tle_line1}\n{tle_line2}\n{'-' * 30}")

        # data_response = session.get(query_url)
        #
        # if data_response.status_code == 200:
        #     print(data_response.json())  # Твои данные тут
        # else:
        #     print(f"Ошибка получения данных: {data_response.status_code}")


def json_data_writer(data):
    pass


if __name__ == "__main__":
    data = take_data_from_site()
    print(data)