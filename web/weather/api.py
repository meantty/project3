import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения для доступа к API
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

def get_coordinates_by_name(city):
    """
    Получает координаты локации по имени города.

    :param city: Имя города для поиска.
    :return: Координаты локации, если удалось получить, иначе (None, None).
    """
    try:
        # Формируем URL для поиска локации по городу
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=ru&format=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['results'][0]  # Извлекаем первый элемент из списка, тк считаем, что он наиболее подходящий
        return {
            'latitude': data['latitude'],
            'longitude': data['longitude']
        }  # Возвращаем координаты
    except Exception as e:
        print(f"Ошибка при получении координат для города {city}: {e}")
        return None, None  # Возвращаем None в случае ошибки


def get_conditions_by_coordinates(latitude=59, longitude=30, days=1):
    """
    Получает данные для построения графиков

    :param latitude: Широта для запроса погодных условий.
    :param longitude: Долгота для запроса погодных условий.
    :param days: Кол-ва дней для прогноза погодных условий.
    :return: Данные для построения графиков предсказания погоды
    """
    try:
        # Формируем URL для получения прогнозов погоды на один день по ключу локации
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,rain,wind_speed_10m&forecast_days={days}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return e  # Обработка ошибок сети
    except (KeyError, IndexError) as e:
        return e  # Обработка ошибок доступа к данным
    except Exception as e:
        return e  # Обработка других ошибок


def get_conditions_by_city(city='Санкт-Петербург', days=1):
    try:
        coordinates = get_coordinates_by_name(city)
        conditions_data = get_conditions_by_coordinates(
            latitude=coordinates['latitude'],
            longitude=coordinates['longitude'],
            days=days
        )
        conditions_data['city'] = city
        return conditions_data
    except Exception as e:
        return e

