# Импорт необходимых классов
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Создание кнопок для основного меню на русском языке
button_category1 = InlineKeyboardButton('💡К вопросам💡', callback_data='К вопросам')
button_category2 = InlineKeyboardButton('📞К номерам📞', callback_data='К номерам')
button_category3 = InlineKeyboardButton('⛪К корпусам⛪', callback_data='К корпусам')
button_category4 = InlineKeyboardButton('🏢Гайд по общежитию🏢', callback_data='Гайд')
button_category5 = InlineKeyboardButton('📖Смена языка📖', callback_data='Смена языка')

# Создание клавиатуры для основного меню на русском языке
keyboard_main_ru = InlineKeyboardMarkup(row_width=1)
keyboard_main_ru.add(button_category1, button_category2, button_category3, button_category4, button_category5)

# Создание кнопок для основного меню на английском языке
button_category_en1 = InlineKeyboardButton('💡Questions💡', callback_data='Questions')
button_category_en2 = InlineKeyboardButton('📞Phone numbers📞', callback_data='Phone numbers')
button_category_en3 = InlineKeyboardButton('⛪Student body⛪', callback_data='Student body')
button_category_en4 = InlineKeyboardButton('🏢Guide to the hostels🏢', callback_data='Guide to the hostels')
button_category_en5 = InlineKeyboardButton('📖Change language📖', callback_data='Change language')

# Создание клавиатуры для основного меню на английском языке
keyboard_main_en = InlineKeyboardMarkup(row_width=1)
keyboard_main_en.add(button_category_en1, button_category_en2, button_category_en3, button_category_en4, button_category_en5)

# Создание кнопок для основного меню на испанском языке
button_category_es1 = InlineKeyboardButton('💡Preguntas💡', callback_data='Preguntas')
button_category_es2 = InlineKeyboardButton('📞Números de teléfono📞', callback_data='Números de teléfono')
button_category_es3 = InlineKeyboardButton('⛪Cuerpo de estudiantes⛪', callback_data='Cuerpo de estudiantes')
button_category_es4 = InlineKeyboardButton('🏢Guía de los albergues🏢', callback_data='Guía de los albergues')
button_category_es5 = InlineKeyboardButton('📖Cambio de idioma📖', callback_data='Cambio de idioma')

# Создание клавиатуры для основного меню на испанском языке
keyboard_main_es = InlineKeyboardMarkup(row_width=1)
keyboard_main_es.add(button_category_es1, button_category_es2, button_category_es3, button_category_es4, button_category_es5)

# Создание кнопок для основного меню на арабском языке
button_category_ar1 = InlineKeyboardButton('💡قائمة الاسئلة💡', callback_data='قائمة الاسئلة')
button_category_ar2 = InlineKeyboardButton('📞جهات الاتصال📞', callback_data='جهات الاتصال')
button_category_ar3 = InlineKeyboardButton('⛪قائمة المباني⛪', callback_data='قائمة المباني')
button_category_ar4 = InlineKeyboardButton('🏢دليل النزل🏢', callback_data='دليل النزل')
button_category_ar5 = InlineKeyboardButton('📖تغير اللغة📖', callback_data='تغير اللغة')

# Создание клавиатуры для основного меню на арабском языке
keyboard_main_ar = InlineKeyboardMarkup(row_width=1)
keyboard_main_ar.add(button_category_ar1, button_category_ar2, button_category_ar3, button_category_ar4, button_category_ar5)

# Создание клавиатуры для выбора языка
language_keyboard = InlineKeyboardMarkup()
language_keyboard.add(InlineKeyboardButton(text="Русский", callback_data="change_language:ru"))
language_keyboard.add(InlineKeyboardButton(text="English", callback_data="change_language:en"))
language_keyboard.add(InlineKeyboardButton(text="Español", callback_data="change_language:es"))
language_keyboard.add(InlineKeyboardButton(text="عرب", callback_data="change_language:ar"))
