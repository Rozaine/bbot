from aiogram.fsm.state import StatesGroup, State


class PromtGPT(StatesGroup):
    promt = State()


class OrderBook(StatesGroup):
    choosing_book_name = State()
    choosing_book = State()