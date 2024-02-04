from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_category1 = InlineKeyboardButton('К вопросам', callback_data='К вопросам')
button_category2 = InlineKeyboardButton('К номерам', callback_data='К номерам')
button_category3 = InlineKeyboardButton('К корпусам', callback_data='К корпусам')
button_category4 = InlineKeyboardButton('Гайд по общежитию', callback_data='Гайд')
button_category5 = InlineKeyboardButton('Смена языка', callback_data='Смена языка')

keyboard_main = InlineKeyboardMarkup(row_width=1)
keyboard_main.add(button_category1, button_category2, button_category3, button_category4, button_category5)

language_keyboard = InlineKeyboardMarkup()
language_keyboard.add(InlineKeyboardButton(text="Русский", callback_data="change_language:ru"))
language_keyboard.add(InlineKeyboardButton(text="English", callback_data="change_language:en"))
language_keyboard.add(InlineKeyboardButton(text="Español", callback_data="change_language:es"))
language_keyboard.add(InlineKeyboardButton(text="عرب", callback_data="change_language:ar"))
