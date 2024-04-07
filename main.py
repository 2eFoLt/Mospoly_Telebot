# Импорт необходимых модулей
import os  # Модуль для работы с операционной системой

# Импорт классов и функций из библиотеки aiogram
from aiogram import types, executor
from aiogram.dispatcher import FSMContext

# Импорт объектов бота и диспетчера команд из созданных модулей
from create_bot import dp, bot
from inline import keyboard_main_ru, keyboard_main_en, keyboard_main_es, keyboard_main_ar, language_keyboard
from database import db_func

# Импорт необходимых функций и классов для работы с markdown и inline клавиатурами
from aiogram.utils.markdown import *


# Функция, выполняемая при старте бота
async def on_startup(_):
    print("Я запустился!")  # Вывод сообщения о запуске бота
    db_func.sql_start()  # Вызов функции для подключения к базе данных


# Помощь для пользователя
HELP_MESSAGE = """Данный бот является помощником для иностранных студентов...
...Если у вас возникли вопросы или проблемы, свяжитесь с нами по электронной почте xxx@example.com"""

# Форматирование текста помощи
my_list = HELP_MESSAGE.split('\n')
result = ""
for item in my_list:
    result += f"\u2022 {item}\n"

# Фразы для выбора языка
language_phrases = {
    'ru': 'Выберите язык:',
    'en': 'Choose a language:',
    'es': 'Elija un idioma:',
    'ar': ':اختر اللغة'
}

# Фразы для изменения языка
change_language_phrases = {
    'ru': 'Язык изменен на русский. Выбирайте нужный раздел:',
    'en': 'Language changed to English. Choose the desired section:',
    'es': 'Idioma cambiado a español. Elija la sección deseada:',
    'ar': 'تم تغيير اللغة إلى العربية . اختر القسم المطلوب:'
}


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # Извлечение идентификатора пользователя из сообщения
    user_id = message.from_user.id
    # Формирование SQL-запроса для вставки идентификатора пользователя в таблицу logs
    sql_query = "INSERT INTO logs (login) VALUES (%s)"
    # Подготовка данных для вставки: идентификатор пользователя
    data = (user_id,)
    # Вызов функции entry_user_id из модуля db_func для выполнения SQL-запроса
    db_func.entry_user_id(sql_query, data)
    # Отправка ответного сообщения пользователю с приветствием и клавиатурой выбора раздела
    await message.reply("Привет! Выбирайте нужный Вам раздел", reply_markup=keyboard_main_ru)


# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    # Удаление входящего сообщения
    await message.delete()
    # Отправка ответного сообщения справки пользователю
    await message.answer(text=result)


# Обработчик нажатия кнопки "Смена языка"
@dp.callback_query_handler(
    lambda x: x.data and x.data in ['Смена языка', 'Change language', 'Cambio de idioma', 'تغير اللغة'])
async def change_language_button(callback_query: types.CallbackQuery, state: FSMContext):
    # Получение текущего выбранного языка из состояния
    data = await state.get_data()
    chosen_language = data.get('chosen_language', 'ru')
    # Получение текста сообщения о выборе языка для текущего языка
    message_text = language_phrases.get(chosen_language, 'Выберите язык:')
    # Отправка сообщения с запросом выбора языка и клавиатурой выбора языка
    await bot.send_message(callback_query.message.chat.id, text=message_text, reply_markup=language_keyboard)
    # Отправка подтверждения обработки запроса
    await callback_query.answer()


# Обработчик нажатия кнопки "Гайд"
@dp.callback_query_handler(
    lambda x: x.data and x.data in ['Гайд', 'Guide to the hostels', 'Guía de los albergues', 'دليل النزل'])
async def process_download_file(callback_query: types.CallbackQuery, state: FSMContext):
    # Получение пути к текущему каталогу скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Получение выбранного языка из состояния
    data = await state.get_data()
    chosen_language = data.get('chosen_language', 'ru')

    # Определение имени файла на основе выбранного языка
    if chosen_language == 'en':
        file_name = 'Guide_for_hostel_residents.pdf'
    elif chosen_language == 'es':
        file_name = 'Guía_para_residentes_de_albergues.pdf'
    elif chosen_language == 'ar':
        file_name = 'دليل للمقيمين في النزل.pdf'
    else:
        file_name = 'Гайд_для_проживающих_в_общежитии.pdf'

    # Формирование полного пути к файлу
    file_path = os.path.join(script_dir, file_name)

    # Проверка существования файла
    if os.path.exists(file_path):
        # Отправка файла пользователю
        with open(file_path, 'rb') as file:
            await bot.send_document(callback_query.from_user.id, file)
        await callback_query.answer()
    else:
        # Уведомление пользователя о том, что файл не найден
        await bot.send_message(callback_query.from_user.id, "Файл не найден")
        await callback_query.answer()


# Обработчик нажатия кнопки "Смена языка"
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("change_language:"))
async def change_language(callback_query: types.CallbackQuery, state: FSMContext):
    # Извлечение кода языка из данных колбэка
    language_code = callback_query.data.split(":")[1]

    # Определение клавиатуры основного меню в зависимости от выбранного языка
    if language_code == 'en':
        keyboard_main = keyboard_main_en
    elif language_code == 'es':
        keyboard_main = keyboard_main_es
    elif language_code == 'ar':
        keyboard_main = keyboard_main_ar
    else:
        keyboard_main = keyboard_main_ru

    # Получение текста сообщения о смене языка для выбранного языка
    message_text = change_language_phrases.get(language_code, 'Язык изменен. Выбирайте нужный раздел:')

    # Обновление данных о выбранном языке в состоянии
    await state.update_data(chosen_language=language_code)

    # Отправка сообщения о смене языка и обновленной клавиатуры основного меню
    await bot.send_message(callback_query.message.chat.id, text=message_text, reply_markup=keyboard_main)
    await callback_query.answer()


# Обработчик нажатия кнопки "К вопросам"
@dp.callback_query_handler(lambda x: x.data and x.data in ['К вопросам', 'Questions', 'Preguntas'])
async def show_questions(callback_query: types.CallbackQuery, state: FSMContext):
    # Получение данных о выбранном языке из состояния
    user_data = await state.get_data()
    current_language = user_data.get("chosen_language", "ru")
    # Получение списка вопросов на выбранном языке
    questions = db_func.get_questions(current_language)

    # Формирование клавиатуры с вопросами
    keyboard_questions = types.InlineKeyboardMarkup(row_width=1)
    for idquestions, question_text in questions:
        keyboard_questions.add(types.InlineKeyboardButton(text=question_text, callback_data=f"question:{idquestions}"))
    # Отправка сообщения со списком вопросов и клавиатурой
    questions_message = await bot.send_message(callback_query.message.chat.id, text='Список вопросов:',
                                               reply_markup=keyboard_questions)

    # Сохранение идентификатора сообщения с вопросами в состоянии
    async with state.proxy() as data:
        data['ref1'] = questions_message.message_id
    # Отправка подтверждения обработки запроса
    await callback_query.answer()


# Обработчик нажатия кнопки "К номерам"
@dp.callback_query_handler(lambda x: x.data and x.data in ['К номерам', 'Phone numbers', 'Números de teléfono'])
async def phone_numbers(callback_query: types.CallbackQuery):
    # Список телефонных номеров и контактов
    numbers = text(
        bold('Приёмная комиссия: '),
        '\n+7 (495) 223-05-23 ',
        '\n+7 (495) 276-37-37 ',
        '\n8 (800) 550-91-42 ',
        bold('\n\nМногофункциональный центр: '),
        '\n+7 (495) 223-05-23 ',
        italic('\nДобавочные номера: '),
        '\nАППАРАТ РЕКТОРА - Руководитель аппарата ректора - Шолохов Олег Викторович : 1102 ',
        '\nПРОРЕКТОР ПО МЕЖДУНАРОДНОЙ ДЕЯТЕЛНОСТИ - Помощник проректора - Гладышева Ирина Юрьевна : 1020 ',
        '\nПРОРЕКТОР ПО ВОСПИТАТЕЛЬНОЙ И СОЦИАЛЬНОЙ РАБОТЕ - Помощник проректора - Мазикина Ирина Игоревна : 1272 ',
        '\nМОБИЛИЗАЦИОННЫЙ ОТДЕЛ - Начальник отдела - Колесников Валерий Алексеевич : 1025 ',
        '\nПРИЕМНАЯ КОМИССИЯ - общий номер : 1640 ',
    )

    # Отправка сообщения с номерами телефонов и контактами
    await bot.send_message(callback_query.message.chat.id, numbers, parse_mode="MARKDOWN")
    await callback_query.answer()


# Обработчик нажатия кнопки "К корпусам"
@dp.callback_query_handler(lambda x: x.data and x.data in ['К корпусам', 'Student body', 'Cuerpo de estudiantes'])
async def academic_buildings(callback_query: types.CallbackQuery):
    # Список адресов учебных корпусов
    acbuilds = text(
        bold("Адрес кампуса на Большой Семёновской: "),
        "\nучебные корпуса «А», «Б», «В», «Н», «НД» ",
        "\nст. м. «Электрозаводская» или ж/д станция Электрозаводская, ул. Б. Семёновская, д. 38. ",
        bold("\n\nАдрес учебного корпуса на станции метро «Автозаводская»: "),
        "\n115280, г. Москва, ул. Автозаводская, д. 16 (ст. м. «Автозаводская»). ",
        bold("\n\nАдрес учебного корпуса на станции метро «ВДНХ»: "),
        "\nул. Павла Корчагина, д. 22. ",
        bold("\n\nАдрес учебного корпуса на улице Прянишникова: "),
        "\n127550, г. Москва, ул. Прянишникова, 2А Корпуса 1, 2 ",
        bold("\n\nАдрес учебного корпуса на улице Михалковская: "),
        "\n125493, г. Москва, ул. Михалковская, д. 7 ",
        bold("\n\nАдрес учебного корпуса на улице Садовая-Спасская: "),
        "\n07045, г. Москва, ул. Садовая-Спасская, д. 6 (ст. м. «Сухаревская») ",
        bold("\n\nАдрес учебного корпуса на станции метро «Авиамоторная»: "),
        "\n111250, г. Москва, ул. Лефортовский вал, д. 26 (ст. м. «Авиамоторная») ",
        bold("\n\nАдрес учебного корпуса «Д» и общежития № 3: "),
        "\nст. м. «Дубровка», ул. 1-я Дубровская, д. 16а. ",
    )

    # Отправка сообщения с адресами учебных корпусов
    await bot.send_message(callback_query.message.chat.id, acbuilds, parse_mode="MARKDOWN")
    await callback_query.answer()


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
