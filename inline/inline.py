from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_category1 = InlineKeyboardButton('К вопросам', callback_data='К вопросам')
button_category2 = InlineKeyboardButton('К номерам', callback_data='К номерам')
button_category3 = InlineKeyboardButton('К корпусам', callback_data='К корпусам')
# button_category4 = InlineKeyboardButton('Назад', callback_data='Назад')

keyboard = InlineKeyboardMarkup(row_width=1)
keyboard.add(button_category1, button_category2, button_category3)
