import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import logic
import os

shop = logic.load_shops()

TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher()
kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Куда сходить сегодня?"), KeyboardButton(text="Список всех секондов")]],
    resize_keyboard=True,
)


@dp.message(Command("start"))
async def hello(message: Message):
    await message.answer(
        "Привет, я телеграм бот, который поможет узнать в каких секондах какие скидки, чтобы ты всегда знал куда зайти!", reply_markup=kb)


@dp.message(Command("where"))
@dp.message(F.text == "Куда сходить сегодня?")
async def hello(message: Message):
    try:
        text = logic.build_where_text()
    except Exception as e:
        print(f"Ошибка в /where: {e}")
        text = "Что-то пошло не так, попробуйте позже."
    await message.answer(text)




@dp.message(Command("list"))
@dp.message(F.text == "Список всех секондов")
async def hello(message: Message):
    try:
        text = logic.build_list_text()
    except Exception as e:
        print(f"Ошибка в /list: {e}")
        text = "Что-то пошло не так, попробуйте позже."
    await message.answer(text)


@dp.message()
async def hello(message: Message):
    await message.answer(f'Нет такой команды')


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
