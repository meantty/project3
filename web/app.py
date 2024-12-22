import json

from flask import Flask, render_template, request, redirect, url_for, jsonify

from telegram_bot.handlers import weather_command
from weather.dash_app import create_dash_app, update_dash_layout
from weather.api import get_conditions_by_city, get_conditions_by_coordinates

app = Flask(__name__)

# Регистрируем Dash-приложение при инициализации Flask-приложения
dash_app = create_dash_app(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Извлекаем начальную, конечную точки и промежуточные точки из формы
        if request.form.get("start_city"):
            start_city = request.form.get("start_city")
        else:
            start_latitude = request.form.get("latitude")
            start_longitude = request.form.get("longitude")
            start_city = (start_latitude, start_longitude)
        end_city = request.form.get("end_city")
        num_points = int(request.form.get("num_intermediate_points", 0))
        forecast_days = int(request.form.get('forecast_days', 1))
        is_bot = request.form.get("is_bot", 0)  # Новый параметр для проверки, является ли запросом от бота


        # Обрабатываем промежуточные точки
        intermediate_cities = [
            request.form.get(f"intermediate_city_{i}")
            for i in range(num_points)
        ]



        # Получаем прогноз погоды для всех точек маршрута
        points = [start_city] + intermediate_cities + [end_city]
        weather_data = []
        for point in points:
            if isinstance(point, tuple):  # Если это координаты
                latitude, longitude = point
                weather_info = get_conditions_by_coordinates(latitude=latitude, longitude=longitude, days=forecast_days)
            else:  # Если это название города
                weather_info = get_conditions_by_city(city=point, days=forecast_days)
            weather_data.append(weather_info)

        # Здесь вызываем функцию для обновления макета Dash
        update_dash_layout(dash_app, weather_data)

        if is_bot:
            # Если запрос от бота, возвращаем только изображения
            images = update_dash_layout(dash_app, weather_data, save_images=True)
            print(images)
            return json.dumps({"images": images}), 200
        # Перенаправляем на страницу с графиками
        return render_template("graphs.html", weather_data=weather_data)

    return render_template("form.html")


@app.route("/graphs")
def show_graphs():
    return render_template("graphs.html")

@app.route("/map")
def show_map():
    # Здесь вы можете обработать полученные данные и передать их в шаблон
    cities_data = request.args.get('cities')
    cities = json.loads(cities_data) if cities_data else []  # Если данные пришли, преобразуем их в список

    return render_template("map.html", cities=cities)


if __name__ == "__main__":
    app.run(debug=True)
