import pandas as pd


def process_weather_data(conditions_data):
    """
        Преобразует JSON-данные погоды в DataFrame для удобного построения графиков.

        :param conditions_data: JSON-данные погоды.
        :return: DataFrame с временными рядами для температуры, влажности, осадков и скорости ветра.
    """

    # Извлекаем данные о времени и метеорологических показателях
    hourly_data = conditions_data.get('hourly', {})

    # Создаем DataFrame из данных
    df = pd.DataFrame({
        'time': hourly_data.get('time', []),
        'temperature': hourly_data.get('temperature_2m', []),
        'humidity': hourly_data.get('relative_humidity_2m', []),
        'rain': hourly_data.get('rain', []),
        'wind_speed': hourly_data.get('wind_speed_10m', [])
    })

    # Преобразуем время в формат datetime
    df['time'] = pd.to_datetime(df['time'])

    return df



