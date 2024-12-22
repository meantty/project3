import os

from dash import Dash, dcc, html
import plotly.graph_objs as go
import plotly.io as pio

from weather.data_processing import process_weather_data


def create_dash_app(flask_app):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')

    # Определяем layout с примером графиков
    dash_app.layout = html.Div(id="dash-container")

    return dash_app


def update_dash_layout(dash_app, weather_data, save_images=False):
    graphs = []
    images = []

    # Проходим по данным для каждого города и создаем графики
    for i, data in enumerate(weather_data):
        try:
            city_name = data['city']
        except KeyError:
            city_name = 'your location'
        # Убедимся, что данные валидные
        if data and 'hourly' in data:
            df = process_weather_data(data)  # Преобразуем данные в DataFrame

            # Создание графика для температуры
            temp_graph = go.Figure(data=[
                go.Scatter(x=df['time'], y=df['temperature'], mode='lines', name='Температура', line=dict(color='blue'))
            ])
            temp_graph.update_layout(title=f'Температура в {city_name}', xaxis_title='Время',
                                     yaxis_title='Температура (°C)')

            # Создание графика для осадков
            precip_graph = go.Figure(data=[
                go.Scatter(x=df['time'], y=df['rain'], mode='lines', name='Осадки', line=dict(color='green'))
            ])
            precip_graph.update_layout(title=f'Осадки в {city_name}', xaxis_title='Время', yaxis_title='Осадки (мм)')

            # Создание графика для скорости ветра
            wind_graph = go.Figure(data=[
                go.Scatter(x=df['time'], y=df['wind_speed'], mode='lines', name='Скорость ветра',
                           line=dict(color='red'))
            ])
            wind_graph.update_layout(title=f'Скорость ветра в {city_name}', xaxis_title='Время',
                                     yaxis_title='Скорость ветра (км/ч)')
            if save_images:
                # Сохраняем изображение
                os.makedirs('images', exist_ok=True)
                image_path = f'images/temp_{city_name}.png'
                pio.write_image(temp_graph, image_path)
                images.append(image_path)

            # Добавляем все графики в список
            graphs.append(html.Div([
                html.H3(f'Прогноз для {city_name}'),
                dcc.Graph(figure=temp_graph, style={'height': '400px'}),
                dcc.Graph(figure=precip_graph, style={'height': '400px'}),
                dcc.Graph(figure=wind_graph, style={'height': '400px'})
            ], id=f"city_{i}_container"))

    # Устанавливаем layout Dash-приложения
    dash_app.layout = html.Div(graphs)

    if images:
        return images
