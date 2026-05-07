import asyncio
import logging
import traceback
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command 
from config import BOT_TOKEN
import keyboard as kb


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_synonyms(word):
    url = "https://api.datamuse.com/words"
    params = {
        "rel_syn": word,
        "max": 10  
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        synonyms = [item['word'] for item in data]
        return str(synonyms)
    except Exception as e:
        with open(file='log.txt', encoding='utf-8', mode='w') as file:
            file.write("---Ошибка---\n")
            traceback.print_exc(file=file)
            file.write("------------")
        return "Something wrong"

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Hello!", reply_markup=kb.main)

@dp.message(Command(commands=['help']))
async def help(message: types.Message):
    await message.reply("Help command")

@dp.message(F.text == "Synonimyze")
async def synonimyze_start(message: types.Message):
    await message.answer("Введите слово для поиска синонимов:")

@dp.message(F.text)
async def process_word(message: types.Message):
    try:
        word = message.text
        if word not in ["Synonimyze"]:
            synonyms = get_synonyms(word)
            await message.answer(f"Синонимы для '{word}':\n{synonyms}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        await dp.start_polling(bot)
    except Exception:
        with open(file='log.txt', encoding='utf-8', mode='w') as file:
            file.write("---Ошибка---\n")
            traceback.print_exc(file=file)
            file.write("------------")
        print("Bot stopped")

if __name__ == '__main__':
    asyncio.run(main())