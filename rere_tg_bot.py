import logging
from aiogram import Bot, Dispatcher, executor, types, filters
from config import TOKEN, WEATHER_TOKEN
from aiogram.dispatcher.filters import Text
import requests
import datetime
import asyncio
 
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level = logging.INFO)

# Create mainKeyboard
@dp.message_handler(commands = "start")
async def main_menu(message: types.Message):
    mainKeyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    # Create mainButtons
    mainButtons = ["My repository", "Contacts", "Show me pussy", "Weather"]
    mainKeyboard.add(*mainButtons)
    # Main Message
    await message.answer("Hello, my name is RERE\nI'm bot for telegram\nI programmed to transmit information", reply_markup = mainKeyboard)

# "My repository"'s button response
@dp.message_handler(lambda message: message.text == "My repository")
async def my_repository(message: types.Message):
    await message.reply("https://github.com/txmxmx/rere_tg_bot.git")

# "Contacts"'s button response
@dp.message_handler(lambda message: message.text == "Contacts")
async def contacts(message: types.Message):
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

# "Show me pussy"'s button response
@dp.message_handler(lambda message: message.text == "Show me pussy")
async def show_pussy(message: types.Message):
    catsKeyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    catsButtons = ["Yes", "No"]
    catsKeyboard.add(*catsButtons)
    await message.answer("Do you want to see my pussy?", reply_markup = catsKeyboard)

# Answer YES
@dp.message_handler(Text(equals = "Yes"))
async def answer_yes(message: types.Message):
    await message.reply("Okay, look")
    await asyncio.sleep(1.5)
    await types.ChatActions.upload_photo()
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('data/img/answer_yes.jpg'))
    await message.reply_media_group(media = media)

# Answer No
@dp.message_handler(Text(equals = "No"))
async def answer_no(message: types.Message):
    await message.reply("Mmm..")
    await asyncio.sleep(1.5)
    await types.ChatActions.upload_photo()
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('data/img/answer_no.jpg'))
    await message.reply_media_group(media = media)

# "Weather"'s button response
@dp.message_handler(lambda message: message.text == "Weather")
async def weather(message: types.Message):
    await message.reply("Okay, enter city name")

# Logics
@dp.message_handler()
async def get_weather(message: types.Message):

    # Code to smile
    codeToSmile = {
        "Clear": "Clear \U0001F917",
        "Clouds": "Clouds \U0001F641",
        "Rain": "Rain \U0001F927",
        "Drizzle": "Drizzle \U0001F927",
        "Thunderstorm": "Thunderstorm \U0001F628",
        "Snow": "Snow \U0001F912",
        "Mist": "Mist \U0001F47B"
    }
    
    # Create logic
    try:
        requestsToWeather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_TOKEN}&units=metric")
        data = requestsToWeather.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weatherDescription = data["weather"][0]["main"]

        if weatherDescription in codeToSmile:
            weatherData = codeToSmile[weatherDescription]
        else:
            weatherData = "Look out the window, I do not understand what the weather is like there!"

        # Search answer
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunriseTimestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunsetTimestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lengthOfTheDay = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        # Create answer
        await message.reply(
            f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"City weather: {city}\nTemperature: {cur_weather}C° {weatherData}\n"
            f"Humidity: {humidity}%\nPressure: {pressure}\nWind: {wind} m\s\n"
            f"Sunrise: {sunriseTimestamp}\nSunset: {sunsetTimestamp}\nDay length: {lengthOfTheDay}\n"
            f"***Have a good day!***"
            )

    except:
        await message.reply("\U0001F914 Check city name \U0001F615")   
   
# Run bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)