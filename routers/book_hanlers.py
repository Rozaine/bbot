from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import Text, Bold

from databaseUtil import mongo_database
from keyboards import common_keyboards
from openAIUtil import get_embedding

router = Router()


class PromtGPT(StatesGroup):
    promt = State()


class OrderBook(StatesGroup):
    choosing_book_name = State()
    choosing_book = State()


@router.message(F.text.lower() == "начать поиск")
async def without_puree(message: types.Message, state: FSMContext):
    await state.update_data(chosen_book=message.text.lower())
    await message.answer("Введите название книги или автора в любом удобном формате.")
    await state.set_state(OrderBook.choosing_book_name)


@router.message(OrderBook.choosing_book_name)
async def book_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_book=message.text.lower())
    user_data = await state.get_data()
    item_count_page = 5
    books_searched = mongo_database.searchBooks(user_data["chosen_book"])

    page_count = round(len(books_searched) / item_count_page)  # TODO if round(len(books_searched) / 12) > 0 else  page

    def func_chunks_generators(lst, n):
        if len(lst) == 0:
            print("empty")
            return
        for i in range(0, len(lst), n):
            yield lst[i: i + n]

    pages_inline_items = list(func_chunks_generators(books_searched, item_count_page))
    page = 1

    try:
        await message.answer("Выберете нужную книгу:",
                             reply_markup=common_keyboards.bookKb(pages_inline_items[0], page_count, page))
    except IndexError:
        await message.answer("Прошу прощения. Не нашел эту книгу.")

    await state.set_state(OrderBook.choosing_book)


@router.callback_query(common_keyboards.Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: common_keyboards.Pagination, state: FSMContext):
    user_data = await state.get_data()
    item_count_page = 5
    books_searched = mongo_database.searchBooks(user_data["chosen_book"])

    page_count = round(len(books_searched) / item_count_page)

    def func_chunks_generators(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i: i + n]

    pages_inline_items = list(func_chunks_generators(books_searched, item_count_page))
    page_num = int(callback_data.page)
    page = page_num

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(pages_inline_items) - 1) else page_num

    if callback_data.action == "prev":
        page = page_num - 1 if page_num - 1 > 0 else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_reply_markup(
            reply_markup=common_keyboards.bookKb(pages_inline_items[page], page_count, page)
        )
    await call.answer()


@router.callback_query(common_keyboards.Pagination.filter(F.action.startswith("dn")))
async def download_handler(call: CallbackQuery, callback_data: common_keyboards.Pagination):
    book_id = callback_data.action[2:]
    book_path = (mongo_database.getBookPathById(book_id)[0]['path'])
    file = FSInputFile(book_path)
    await call.message.answer_document(file)
    await call.answer(callback_data.action)


@router.message(F.text.lower() == "chatgpt, посоветуй книгу")
async def without_puree(message: types.Message, state: FSMContext):
    await state.update_data(promt=message.text.lower())
    await message.answer("Опишите какую книгу вы бы хотели чтобы я вам посоветовал. "
                         "Функция может работать нестабильно.")
    await state.set_state(PromtGPT.promt)


@router.message(PromtGPT.promt)
async def generateBookRecommendation(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    openAnswer = await get_embedding(user_data['promt'])
    content = Text('Я могу вам посоветовать: ',
                   Bold(openAnswer.replace('.', '')),
                   '. Возможно вам понравится эта книга!')
    await message.answer(**content.as_kwargs())
    await state.clear()
