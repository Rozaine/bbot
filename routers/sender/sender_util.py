import asyncio
import time
from typing import Dict, List

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def generate_kb(
        btn_text: str = None,
        btn_url: str = None,
) -> InlineKeyboardMarkup | None:
    btn_builder = InlineKeyboardBuilder()
    btn_builder.row(
        InlineKeyboardButton(
            text=btn_text,
            url=btn_url,
        )
    )
    return btn_builder.as_markup()


async def send_preview_with_kb(
        message,
        photo: str = None,
        text: str = '',
        btn_text: str = None,
        btn_url: str = None,
) -> int:
    keyboard = generate_kb(btn_text, btn_url)
    send_msg = await message.answer_photo(caption=text, photo=photo, reply_markup=keyboard,
                                          parse_mode=ParseMode.MARKDOWN_V2)
    return send_msg.message_id


async def send_preview(message: Message, data: Dict) -> int:
    message_id = await send_preview_with_kb(
        message,
        data["msg_photo"],
        data["msg_text"],
        data["btn_text"],
        data["btn_url"],
    )
    return message_id


async def send_mail(
        bot: Bot,
        user_id: str,
        from_chat_id: int,
        message_id: int,
        keyboard: InlineKeyboardMarkup = None
) -> bool:
    try:
        await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id, reply_markup=keyboard)
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_mail(bot, user_id, from_chat_id, message_id, keyboard)
    except Exception as e:
        print(e)
        # TODO ADD USER ACTIVE STATUS
        return False
    else:
        return True


async def start_sender(
        bot: Bot,
        data: Dict,
        user_id: List[str],
        from_chat_id: int,
        message_id: int
) -> int:
    count = 0
    keyboard = generate_kb(data["btn_text"], data["btn_url"])
    for i in user_id:
        if await send_mail(bot, i, from_chat_id, message_id, keyboard):
            count += 1
        await asyncio.sleep(0.05)
    return count
