from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import config
from openAIUtil import get_embedding
from keyboards import common_keyboards
from databaseUtil import common as sql, mongo_database as mongo

router = Router()


@router.message(Command("admin"))
async def without_puree(message: types.Message):
    if message.from_user.id == int(config.ADMIN_ID):
        keyboard = types.ReplyKeyboardMarkup(keyboard=common_keyboards.admin_kb, resize_keyboard=True)
        await message.answer("Успешно!", reply_markup=keyboard)


@router.message(F.text.lower() == "статистика")
async def without_puree(message: types.Message):
    if message.from_user.id == int(config.ADMIN_ID):
        keyboard = types.ReplyKeyboardMarkup(keyboard=common_keyboards.admin_kb, resize_keyboard=True)
        all_users = sql.getAllUsersCount()
        reg_today = sql.getTodayRegUsersCount()
        # booksCount = mongo.getCountBooks() # TODO CONNECT MONGODB
        content = f"Все юзеры: {all_users}, за сегодня рег: {reg_today}"
        await message.answer(str(content), reply_markup=keyboard)
