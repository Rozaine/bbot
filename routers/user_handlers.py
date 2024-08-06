from aiogram import types, Router, F
from aiogram.types import Message
from aiogram.filters import Command

from databaseUtil import common as sql, mongo_database as mongo

from keyboards.common_keyboards import main_kb

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard=True)
    if sql.hasRegistered(msg):
        sql.updateLastUserActivity(msg)
    else:
        sql.registerUser(msg)
    await msg.answer("Привет! Я помогу тебе найти книги, чтобы начать нажми кнопку 'Начать поиск'.",
                     reply_markup=keyboard)


@router.message(Command("help"))
async def start_handler(msg: Message):
    sql.updateLastUserActivity(msg)
    keyboard = types.ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard=True)
    await msg.answer("По любым вопросам: @roza1ne", reply_markup=keyboard)


@router.message(F.text.lower() == "случайная книга")
async def without_puree(message: types.Message):
    await message.answer("Пока что не доступно - в работе")


@router.message(F.text.lower() == "без рекламы")
async def without_puree(message: types.Message):
    await message.answer("Пока что не доступно - в работе")


@router.message()
async def message_handler(msg: Message):
    sql.updateLastUserActivity(msg)
    await msg.answer(f"Не понял команду, воспользуйся /help")
