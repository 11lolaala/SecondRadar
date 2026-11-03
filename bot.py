import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logic
import os

shop = logic.load_shops()

TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher()
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Куда сходить сегодня?"), KeyboardButton(text="Список всех секондов")],
        [KeyboardButton(text="Выбрать дату")]],
    resize_keyboard=True,
)


class PickDate(StatesGroup):
    waiting = State()


@dp.message(Command("start"))
async def hello(message: Message):
    await message.answer(
        "Привет, я телеграм бот, который поможет узнать в каких секондах какие скидки, чтобы ты всегда знал куда зайти!",
        reply_markup=kb)


@dp.message(Command("where"))
@dp.message(F.text == "Куда сходить сегодня?")
async def where(message: Message):
    try:
        text = logic.build_where_text()
    except Exception as e:
        print(f"Ошибка в /where: {e}")
        text = "Что-то пошло не так, попробуйте позже."
    await message.answer(text)


@dp.message(Command("list"))
@dp.message(F.text == "Список всех секондов")
async def list_shop(message: Message):
    try:
        text = logic.build_list_text()
    except Exception as e:
        print(f"Ошибка в /list: {e}")
        text = "Что-то пошло не так, попробуйте позже."
    await message.answer(text)


@dp.message(F.text == "Выбрать дату")
async def choose_date(message: Message, state: FSMContext):
    await message.answer("Введите дату, например 05.11")
    await state.set_state(PickDate.waiting)


@dp.message(PickDate.waiting)
async def processing_date(message: Message, state: FSMContext):
    try:
        date_raw = logic.get_date(message.text)
    except ValueError as e:
        print(f"Не понял дату {e} def processing_date")
        await message.answer("Не понял дату, попробуй ещё раз, например 05.11")
        return
    try:
        text = logic.build_list_text(date_raw)
    except Exception as e:
        print(f"Ошибка в списке: {e}")
        text = "Что-то пошло не так, попробуй позже"
    await message.answer(text)
    await state.clear()


@dp.message()
async def unknow_command(message: Message):
    await message.answer(f'Нет такой команды')


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
