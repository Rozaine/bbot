from aiogram.types import KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_kb = [
    [KeyboardButton(text="🔍 Начать поиск")],
    # [KeyboardButton(text="Случайная книга"), KeyboardButton(text="Без рекламы")],
]

admin_kb = [
    [KeyboardButton(text="Ban/unban"), KeyboardButton(text="Сделать рассылку")],
    [KeyboardButton(text="Статистика"), KeyboardButton(text="Отправить рассылку")],
]


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


class Maling(CallbackData, prefix="mail"):
    action: str


def get_kb_confirm() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Send now', callback_data=Maling(action='start').pack()),
        InlineKeyboardButton(text='Stop', callback_data=Maling(action='stop').pack())
    )
    return builder


def bookKb(book_list: list, pages_value: int, page: int) -> InlineKeyboardMarkup:
    buttons = []

    for i in book_list:
        user_button = [
            InlineKeyboardButton(text=f"{i['author']} - {i['title']} ",
                                 callback_data=Pagination(action=f'dn{i["_id"]}', page=page).pack())
        ]
        buttons.append(user_button)

    bottom_buttons = [InlineKeyboardButton(text="⬅️", callback_data=Pagination(action='prev', page=page).pack()),
                      InlineKeyboardButton(text=f"{page}/{pages_value}", callback_data="page_num"),
                      InlineKeyboardButton(text="➡️", callback_data=Pagination(action='next', page=page).pack())]

    buttons.append(bottom_buttons)

    keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)

    return keyboard
