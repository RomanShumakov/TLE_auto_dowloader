import os
from dotenv import load_dotenv
import requests

load_dotenv()

def take_data_from_site():
    url = "https://www.space-track.org/app/data/whoami"
    # url = "https://www.space-track.org/basicspacedata/query/class/gp/EPOCH/>now-30/MEAN_MOTION/>11.25/format/3le"
    api_key = os.getenv('API_KEY')
    headers = {
        "apikey": api_key
    }
    datas = requests.get(url, headers=headers)
    # data = requests.get(url, headers=headers, params=params)
    # data = requests.get(url)

    return datas

def neuro_help():
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
    if response.status_code == 200:
        print("Авторизация прошла успешно!")
        authorisation = session.get("https://www.space-track.org/app/data/whoami")

        data = authorisation.json()  # Превращаем ответ в словарь
        print(f'Пользователь: {data["identity"]} Активность: {data["logged_in"]}')


        # 2. Теперь делаем сам запрос за данными (например, TLE)
        query_url = 'https://www.space-track.org/basicspacedata/query/class/satcat/limit/1/format/json'


        data_response = session.get(query_url)

        if data_response.status_code == 200:
            print(data_response.json())  # Твои данные тут
        else:
            print(f"Ошибка получения данных: {data_response.status_code}")
    else:
        print("Не удалось залогиниться, проверь почту и пароль.")


def json_data_writer(data):
    pass


if __name__ == "__main__":
    data = neuro_help()
    print(data)