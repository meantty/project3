# telegram_bot/handlers.py
import os

from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InputFile, \
    FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import requests
import json

API_BASE_URL = "http://127.0.0.1:5000"  # URL основного веб-сервиса

class WeatherStates(StatesGroup):
    start_city = State()
    end_city = State()
    forecast_days = State()

# Команда /start
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я помогу тебе получить прогноз погоды для заданного маршрута. "
        "Отправь /weather, чтобы начать или /help для списка команд."
    )

# Команда /help
async def help_command(message: types.Message):
    await message.answer(
        "/start - Начать работу с ботом\n"
        "/weather - Получить прогноз погоды по маршруту\n"
        "/help - Помощь по командам"
    )

# Команда /weather для начала запроса погоды
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Команда /weather для начала запроса погоды
async def weather_command(message: types.Message, state: FSMContext):
    location_button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить местоположение", request_location=True)]
        ],
        resize_keyboard=True
    )
    await message.answer("Введите начальную точку маршрута (город) или отправьте свое местоположение:", reply_markup=location_button)
    await state.set_state(WeatherStates.start_city)


# Обработка ввода начальной точки
async def process_start_city(message: types.Message, state: FSMContext):
    if message.location:  # Check if the message has location data
        # Extract coordinates
        latitude = message.location.latitude
        longitude = message.location.longitude
        await state.update_data(latitude=latitude, longitude=longitude)
    else:
        await state.update_data(start_city=message.text)
    await message.answer("Введите конечную точку маршрута (город):")
    await state.set_state(WeatherStates.end_city)

# Обработка ввода конечной точки
async def process_end_city(message: types.Message, state: FSMContext):
    await state.update_data(end_city=message.text)

    # Создаем инлайн-кнопки для выбора дней прогноза
    buttons = [
        InlineKeyboardButton(text="Прогноз на 1 день", callback_data="days_1"),
        InlineKeyboardButton(text="Прогноз на 3 дня", callback_data="days_3"),
        InlineKeyboardButton(text="Прогноз на 7 дней", callback_data="days_7")
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.answer("Выберите период прогноза:", reply_markup=keyboard)
    await state.set_state(WeatherStates.forecast_days)

# Обработка выбора периода прогноза
async def forecast_days_callback(callback_query: types.CallbackQuery, state: FSMContext):
    forecast_days = int(callback_query.data.split("_")[1])
    await state.update_data(forecast_days=forecast_days)
    data = await state.get_data()

    # Запрашиваем данные у веб-сервиса
    try:
        response = requests.post(
            f"{API_BASE_URL}/",
            data={
                "start_city": data["start_city"],
                "end_city": data["end_city"],
                "forecast_days": forecast_days,
                "num_intermediate_points": 0,
                "is_bot": 1
            }
        )
    except:
        response = requests.post(
            f"{API_BASE_URL}/",
            data={
                "latitude": data['latitude'],
                "longitude": data['longitude'],
                "end_city": data["end_city"],
                "forecast_days": forecast_days,
                "num_intermediate_points": 0,
                "is_bot": 1
            }
        )

    if response.status_code == 200:
        # Получаем список путей к изображениям графиков от API
        image_paths = response.json().get("images")
        if image_paths:
            # Отправляем изображения графиков
            for image_path in image_paths:
                try:
                    # Construct the full path to the image
                    full_image_path = '../' + image_path  # Adjust the path as necessary
                    # Check if the file exists before creating InputFile
                    if os.path.exists(full_image_path):
                        photo = FSInputFile(full_image_path)  # Use the file path directly
                        await callback_query.message.answer_photo(photo)
                    else:
                        await callback_query.message.answer(f"Image file not found at path: {full_image_path}")
                except Exception as e:
                    await callback_query.message.answer(f"An error occurred: {str(e)}")
        else:
            await callback_query.message.answer("Не удалось получить графики.")
    else:
        await callback_query.message.answer("Ошибка при попытке получить данные. Попробуйте позже.")

    await state.clear()  # Сбрасываем состояние

# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
    dp.message.register(help_command, Command("help"))
    dp.message.register(weather_command, Command("weather"))
    dp.message.register(process_start_city, WeatherStates.start_city)
    dp.message.register(process_end_city, WeatherStates.end_city)
    dp.callback_query.register(forecast_days_callback, F.data.startswith("days_"))
