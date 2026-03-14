"""
Ushbu modul OpenWeatherMap API orqali 3 kunlik ob-havo ma'lumotlarini olish va formatlash uchun funksiyalarni o'z ichiga oladi.
"""
import asyncio
from datetime import datetime, timedelta


import aiohttp
import telebot

from config import TOKEN

API_KEY = "79c120c481aac4f0c994f4bc121b5cc8"


telebot = telebot.TeleBot(TOKEN)


def weather_text(condition: str) -> str:
    """Ob-havo holatiga mos emoji qaytaradi."""
    condition = condition.lower()
    if "clear" in condition or "sun" in condition:
        return "☀️ Quyoshli"
    if "cloud" in condition:
        return "⛅️ Bulutli"
    if "rain" in condition:
        return "🌧 Yomg‘ir"
    if "snow" in condition:
        return "❄️ Qor"
    return "🌥 Ozgaruvchan"


async def get_owm_weather(lat: str, lon: str):
    """OpenWeatherMap API orqali ob-havo ma'lumotlarini oladi (koordinata bilan)."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data


def format_owm_forecast(data):
    """OpenWeatherMap API dan olingan ma'lumotlarni formatlaydi."""
    msg = "Salom hammaga"
    "\n\n🌤 Andijon viloyati 3 kunlik ob-havo ma'lumotlari\n\n"
    msg += f"📍 Oqdaryo tumani\n\n"

    today = datetime.now().date()
    days_name = ["Bugun", "Ertaga", "Indinga"]


    for i in range(3):
        day_date = today + timedelta(days=i)
        forecast = next((f for f in data['list'] if datetime.fromtimestamp(f['dt']).date() == day_date and datetime.fromtimestamp(f['dt']).hour == 12), None)
        if not forecast:
            forecast = next((f for f in data['list'] if datetime.fromtimestamp(f['dt']).date() == day_date), None)

        if forecast:
            weather = forecast['weather'][0]['main']
            temp_max = round(forecast['main']['temp_max'])
            temp_min = round(forecast['main']['temp_min'])
            wind = round(forecast['wind']['speed'])
            rain = round(forecast.get('pop', 0) * 100)

            emoji = weather_text(weather)
            msg += f"📅 {days_name[i]}:\n\n"
            msg += f"{emoji}\n"
            msg += f"🌡 +{temp_max}°C / +{temp_min}°C\n"
            msg += f"💨 Shamol: {wind} m/s\n"
            msg += f"🌧 Yogingarchilik ehtimoli: {rain}%\n\n"


    return msg


def get_andijon_weather():
    """Andijon viloyati ob-havo ma'lumotlarini olish va konsolga chiqarish."""
    lat = 40.7450
    lon = 72.3500


    data = asyncio.run(get_owm_weather(lat, lon))
    message = format_owm_forecast(data)


    telebot.send_message(-1003130885017, message)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Andijon ob-havo:\n{message}")
