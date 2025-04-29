from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Получение данных")],
],
resize_keyboard=True,
input_field_placeholder="Выберите пункт меню"
)

main_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Получение данных")],
    [KeyboardButton(text="Add data")], 
    [KeyboardButton(text="Change data")]
],
resize_keyboard=True,
input_field_placeholder="Выберите пункт меню"
)

getdata = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="За 7 дней", callback_data="data_last7days")],
    [InlineKeyboardButton(text="За 14 дней", callback_data="data_last14days")],
    [InlineKeyboardButton(text="По дате", callback_data="by_date")],
])
    
