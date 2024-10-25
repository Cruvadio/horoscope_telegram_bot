
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from keyboards.all_kb import create_rat, create_inline
from utils.globals import HOROSCOPE_SIGNS
from db_handler.db_handler import get_user_data, insert_user
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.horoscope import make_horoscope
start_router = Router()
from datetime import date
from create_bot import pg_manager, bot
class Horoscope(StatesGroup):
    none = State()
    sign = State()
commands = ["/clear_history", "/update", "/change_zodiac", "/start"]
async def show_horoscope(user_id, chat_id):
    data = await get_user_data(user_id)
    if not data:
        return None
    text, photo = make_horoscope(data)
    async with pg_manager:
        today_date = await pg_manager.select_data(table_name="messages", where_dict=[{"chat_id": chat_id, "date": date.today()}])
        if today_date:
            await bot.edit_message_caption(caption=text, reply_markup=create_inline(), chat_id=chat_id, message_id=today_date[0]["message_id"])
        else:
            msg_id = await bot.send_photo(photo=photo, caption=text, reply_markup=create_inline(), chat_id=chat_id)
            await pg_manager.insert_data_with_update(table_name="messages",
                                           records_data={"message_id": msg_id.message_id,
                                                         "chat_id": chat_id,
                                                         "date": date.today()
                                                         },
                                           update_on_conflict=False,
                                                     conflict_column="chat_id")
@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, scheduler: AsyncIOScheduler):
    await state.set_state(Horoscope.sign)
    async with pg_manager:
        await pg_manager.delete_data(table_name="messages", where_dict={"chat_id": message.chat.id})
    await message.answer('Выберете свой знак зодиака!', reply_markup=create_rat())


@start_router.message(Command('change_zodiac'))
async def change_zodiac(message: Message, state: FSMContext):
    await state.set_state(Horoscope.sign)
    async with pg_manager:
        await pg_manager.delete_data(table_name="messages", where_dict={"chat_id": message.chat.id})
    await message.answer('Выберете свой знак зодиака!', reply_markup=create_rat())
@start_router.message(F.text.in_(HOROSCOPE_SIGNS), Horoscope.sign)
async def register_sign (message: Message, state: FSMContext , scheduler: AsyncIOScheduler):
    sign = ""
    match message.text:
        case "♈️":
            sign = 'Овен'
        case "♉️":
            sign = 'Телец'
        case "♊️":
            sign = 'Близнецы'
        case "♋️":
            sign = 'Рак'
        case "♌️":
            sign = 'Лев'
        case "♍️":
            sign = 'Дева'
        case "♎️":
            sign = 'Весы'
        case "♏️":
            sign = 'Скорпион'
        case "♐️":
            sign = 'Стрелец'
        case "♑️":
            sign = 'Козерог'
        case "♒️":
            sign = 'Водолей'
        case "♓️":
            sign = 'Рыбы'
    await state.update_data(sign=sign)
    user_data = {"user_id": message.from_user.id, "sign": sign, "chat_id": message.chat.id}
    await insert_user(user_data)
    msg_text = (f'Ваш знак зодиака - <b>{sign}</b>')
    await message.answer(msg_text)
    await show_horoscope(message.from_user.id, message.chat.id)
    await state.set_state(Horoscope.none)





@start_router.message(Command("clear_history"))
async def clear_history (message: Message, state:FSMContext):
    async with pg_manager:
        chat_messages = await pg_manager.select_data(table_name="messages", where_dict=[{"chat_id": message.chat.id}])
        await pg_manager.delete_data(table_name="messages", where_dict=[{"chat_id": message.chat.id}])
        if chat_messages:
            for message in chat_messages:
                await bot.delete_message(chat_id=message["chat_id"], message_id=message["message_id"])


@start_router.message(Command('update'))
async def update_horoscope (message: Message, state:FSMContext):
    await show_horoscope(message.from_user.id, message.chat.id)

@start_router.callback_query(F.data == 'update')
async def callback_update (call: CallbackQuery, state:FSMContext):
    data = await get_user_data(call.from_user.id)
    if not data:
        return None
    text, photo = make_horoscope(data)
    await call.message.edit_caption(caption=text, reply_markup=create_inline())

@start_router.message(F.text)
async def default_handler (message: Message):
    await message.answer("Извините, я не понял.")
async def send_horoscope():
    async with pg_manager:
        users = await pg_manager.select_data(table_name="users")
        if not users:
            return None
        for user in users:
            await show_horoscope(user["user_id"], user["chat_id"])

