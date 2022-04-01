import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from aiogram.dispatcher.filters import Text

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Create mainKeyboard
@dp.message_handler(commands = "start")
async def cmd_start(message: types.Message):
    mainKeyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    # Create mainButtons
    mainButtons = ["My repository", "Contacts"]
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
   
# Run bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)