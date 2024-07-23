from aiogram.fsm.state import StatesGroup, State


class PromtGPT(StatesGroup):
    promt = State()


class OrderBook(StatesGroup):
    choosing_book_name = State()
    choosing_book = State()


class CreateMessage(StatesGroup):
    get_text = State()
    get_photo = State()
    get_keyboard_text = State()
    get_keyboard_url = State()
    confirm_send = State()
