import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, WEATHER_TOKEN
from aiogram.dispatcher.filters import Text

import requests
import datetime

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Create mainKeyboard
@dp.message_handler(commands = "start")
async def cmd_start(message: types.Message):
    mainKeyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    # Create mainButtons
    mainButtons = ["My repository", "Contacts", "Weather"]
    mainKeyboard.add(*mainButtons)
    # Main Message
    await message.answer("Hello, my name is RERE\nI'm bot for telegram\nI programmed to transmit information", reply_markup = mainKeyboard)
   
# "My repository"'s button response
@dp.message_handler(lambda message: message.text == "My repository")
async def without_puree(message: types.Message):
    await message.reply("https://github.com/txmxmx/rere_tg_bot.git")

# "Contacts"'s button response
@dp.message_handler(lambda message: message.text == "Contacts")
async def cmd_inline_url(message: types.Message):
    # Create contactsButtons
    contactsButtons = [
        types.InlineKeyboardButton(text="Site", url= "http://txmxmx.ru/"),
        types.InlineKeyboardButton(text="Telegram", url = "https://t.me/tmmyR6"),
        types.InlineKeyboardButton(text="AtrStation", url = "https://txmxmx.artstation.com/")
    ]
    contactsKeyboard = types.InlineKeyboardMarkup(row_width = 1)
    contactsKeyboard.add(*contactsButtons)
    # Message
    await message.answer("Links to contacts", reply_markup = contactsKeyboard)

# "Weather"'s button response
@dp.message_handler(lambda message: message.text == "Weather")
async def start_command(message: types.Message):
    await message.reply("Okay, Enter city name")

# Logics
@dp.message_handler()
async def get_weather(message: types.Message):
    # Smiles's codes
    code_to_smile = {
        "Clear": "Clear \U0001F917",
        "Clouds": "Clouds \U0001F641",
        "Rain": "Rain \U0001F927",
        "Drizzle": "Drizzle \U0001F927",
        "Thunderstorm": "Thunderstorm \U0001F628",
        "Snow": "Snow \U0001F912",
        "Mist": "Mist \U0001F47B"
    }
    
    # Create requests
    try:
        requests_to_weather = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_TOKEN}&units=metric")
        data = requests_to_weather.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Look out the window, I do not understand what the weather is like there!"

        # Search answer
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        # Create answer
        await message.reply(
            f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"City weather: {city}\nTemperature: {cur_weather}C° {wd}\n"
            f"Humidity: {humidity}%\nPressure: {pressure}\nWind: {wind} m\s\n"
            f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nDay length: {length_of_the_day}\n"
            f"***Have a good day!***"
            )

    except:
        await message.reply("\U0001F914 Check city name \U0001F615")       
   
# Run bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)