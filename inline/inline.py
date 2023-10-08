from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_category1 = InlineKeyboardButton('Опция 1', callback_data='Опция 1')
button_category2 = InlineKeyboardButton('Опция 2', callback_data='Опция 2')
button_category3 = InlineKeyboardButton('Опция 3', callback_data='Опция 3')
button_category4 = InlineKeyboardButton('Назад', callback_data='Назад')

keyboard = InlineKeyboardMarkup(row_width=1)
keyboard.add(button_category1, button_category2, button_category3, button_category4)
