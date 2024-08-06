import time

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import config
from keyboards import common_keyboards
from keyboards.common_keyboards import get_kb_confirm
from routers.states import CreateMessage

from .sender_util import send_preview, start_sender, bot

router = Router()


@router.message(CreateMessage.get_text, F.text)
async def set_text_handler(message: Message, state: FSMContext):
    await state.update_data(msg_text=message.md_text)
    await message.answer(
        text="Пришлите фото."
    )
    await state.set_state(CreateMessage.get_photo)


@router.message(CreateMessage.get_photo, F.photo)
async def set_photo_handler(message: Message, state: FSMContext):
    await state.update_data(msg_photo=message.photo[-1].file_id)
    data = await state.get_data()
    await state.set_state(CreateMessage.get_keyboard_text)
    await message.answer(
        text="Пришлите текст для кнопки"
    )


@router.message(CreateMessage.get_keyboard_text, F.text)
async def set_kb_text_handler(message: Message, state: FSMContext):
    await state.update_data(btn_text=message.text)
    await state.set_state(CreateMessage.get_keyboard_url)
    await message.answer(
        text="Пришлите url для кнопки"
    )


@router.message(CreateMessage.get_keyboard_url, F.text)
async def set_kb_url_handler(message: Message, state: FSMContext):
    await state.update_data(btn_url=message.text)
    data = await state.get_data()
    message_id = await send_preview(
        message,
        data
    )
    await state.update_data(message_id=message_id)
    await message.answer(
        text='Проверьте',
        reply_markup=get_kb_confirm().as_markup(),
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(CreateMessage.confirm_send)


@router.callback_query(common_keyboards.Maling.filter(F.action.startswith("stop")))
async def cancel_sending(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Рассылка отменена')
    await state.clear()
    await callback.answer()


@router.callback_query(common_keyboards.Maling.filter(F.action.startswith("start")))
async def start_sending(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer('Рассылка началась')
    await state.clear()
    await callback.answer()

    user_id = [str(config.ADMIN_ID), "393364862"]  # TODO GET REAL USERS
    t_start = time.time()
    msg_id = data.get('message_id')
    count = await start_sender(
        bot=bot,
        data=data,
        user_id=user_id,
        from_chat_id=callback.message.chat.id,
        message_id=msg_id
    )
    await callback.message.answer(f'Отправлено {count}/{len(user_id)} за {round(time.time() - t_start)} s.')
