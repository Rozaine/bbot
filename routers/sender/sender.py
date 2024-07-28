from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.common_keyboards import get_kb_confirm
from routers.states import CreateMessage

from .sender_util import send_preview

router = Router()


@router.message(CreateMessage.get_text, F.text)
async def set_text_handler(message: Message, state: FSMContext):
    await state.update_data(msg_text=message.md_text)
    await message.answer(
        text="All right, now photo"
    )
    await state.set_state(CreateMessage.get_photo)


@router.message(CreateMessage.get_photo, F.photo)
async def set_photo_handler(message: Message, state: FSMContext):
    await state.update_data(msg_photo=message.photo[-1].file_id)
    data = await state.get_data()
    await state.set_state(CreateMessage.get_keyboard_text)
    await message.answer(
        text="All right, now keyboard text"
    )


@router.message(CreateMessage.get_keyboard_text, F.text)
async def set_kb_text_handler(message: Message, state: FSMContext):
    await state.update_data(btn_text=message.text)
    await state.set_state(CreateMessage.get_keyboard_url)
    await message.answer(
        text="All right, now keyboard url"
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
        text='Done, check it out.',
        reply_markup=get_kb_confirm().as_markup(),
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(CreateMessage.confirm_send)
