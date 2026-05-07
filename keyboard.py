from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Synonimyze")]], resize_keyboard=True, 
    input_field_placeholder="Введите слово для синонимизации на английском")