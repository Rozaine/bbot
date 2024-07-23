from aiogram import types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import config
from keyboards import common_keyboards
from databaseUtil import common as sql, mongo_database as mongo

from .states import CreateMessage

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


@router.message(F.text.lower() == "отправить рассылку")
async def make_newsletter(message: types.Message, state: FSMContext):
    adminID = config.ADMIN_ID
    await message.answer('Send message text', parse_mode=ParseMode.MARKDOWN)
    await state.set_state(CreateMessage.get_text)
