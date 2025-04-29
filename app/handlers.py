from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config.conf import ADMINKA
import app.keyboard as kb
from app.backend import add_day, change_day, get_info_by_date, get_info_from_file_last7days, get_info_from_file_last14days, force_add_data

router = Router()

# ------------ States ---------------------------

class Add_Data(StatesGroup):
    lesson = State()

class Get_Data(StatesGroup):
    date = State()

class Change_Data(StatesGroup):
    date = State()
    lesson = State()

# -----------------------------------------------

@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id in ADMINKA:
        await message.answer("Успешная авторизация\nadmin permissions", reply_markup=kb.main_admin)
    else:
        await message.answer("Успешная авторизация", reply_markup=kb.main)
    
# ------------ Debug func -----------------------

@router.message(Command("debuginfo"))
async def get_info(message: Message):
    await message.reply(f"Your ID - {message.from_user.id}\nYour Name - {message.from_user.first_name}\nYour username - {message.from_user.username}")

@router.message(Command("ping"))
async def get_info(message: Message):
    await message.answer("pong")

# ------------ Update func ----------------------
@router.message(F.text == "Get data")
async def get_data(message: Message):
    update_text = "Бот обновлен 0.7.4 -> 0.7.5\nChangelog:\nПереведены кнопки с забугорного на русский"
    if message.from_user.id in ADMINKA:
        await message.answer(update_text, reply_markup=kb.main_admin)
    else:
        await message.answer(update_text, reply_markup=kb.main)

# ------------ Admin funcs ----------------------

# Change data
@router.message(F.text == "Change data")
async def change_data_by_date(message: Message, state: FSMContext):
    if message.from_user.id in ADMINKA:
        await state.set_state(Change_Data.date)
        await message.answer("Введите дату в формате (xx.xx)")

@router.message(Change_Data.date)
async def get_data_to_change(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    await message.answer("Введите новое значение (число, либо \"-\")")
    await state.set_state(Change_Data.lesson)
@router.message(Change_Data.lesson)
async def get_lesson_to_change(message: Message, state: FSMContext):
    await state.update_data(lesson=message.text)
    data = await state.get_data()
    await message.answer(change_day(data["date"], data["lesson"]))
    await state.clear()

# Add data
@router.message(F.text == "Add data")
async def add_data_one(message: Message, state: FSMContext):
    if message.from_user.id in ADMINKA:
        await state.set_state(Add_Data.lesson)
        await message.answer("К какому уроку подошел?\n(Номер урока, либо \"-\")")
    
@router.message(Add_Data.lesson)
async def add_data_two(message: Message, state: FSMContext):
    await state.update_data(lesson=message.text)
    data = await state.get_data()
    await message.answer(add_day(data["lesson"]))
    await state.clear()

async def force_data_check(bot: Bot):
    if force_add_data():
        await bot.send_message(1132011077, f"WARNING\nToday's date value is set to -1, please change the value")
        
# -------------- User Func -----------------------    

@router.message(F.text == "Получение данных")
async def get_data(message: Message):
    await message.answer("Выберите период времени", reply_markup=kb.getdata)

@router.callback_query(F.data == "data_last7days")
async def data_last7days(callback: CallbackQuery):
    await callback.message.edit_text(get_info_from_file_last7days())

@router.callback_query(F.data == "data_last14days")
async def data_last14days(callback: CallbackQuery):
    await callback.message.edit_text(get_info_from_file_last14days())

@router.callback_query(F.data == "by_date")
async def po_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Get_Data.date)
    await callback.message.edit_text("Введите дату в формате (xx.xx)\nСтатистика ведется с начала 2025 года")

@router.message(Get_Data.date)
async def get_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    await message.answer(get_info_by_date(data["date"]))
    await state.clear()
