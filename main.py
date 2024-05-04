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

# Обработчик вывода ответа на нужный вопрос
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("question:"))
async def show_answers(callback_query: types.CallbackQuery, state: FSMContext):
    question_id = int(callback_query.data.split(":")[1])

    state_data = await state.get_data()
    current_language = state_data.get("chosen_language", "ru")

    answers = db_func.get_answers(question_id, current_language)

    answer_text = "\n".join(answer for (answer,) in answers)
    answer_message = await bot.send_message(callback_query.message.chat.id, text=f'{answer_text}')
    answer_message_id = answer_message.message_id
    async with state.proxy() as data:
        questions_message_id = data['ref1']
    if (int(answer_message_id) - int(questions_message_id)) > 1:
        await callback_query.bot.delete_message(callback_query.message.chat.id, answer_message_id - 1)
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
async def phone_numbers(callback_query: types.CallbackQuery, state: FSMContext):
    # Получаем текущий язык из состояния
    data = await state.get_data()
    chosen_language = data.get('chosen_language', 'ru')  # Если язык не выбран, используем русский
    # Список телефонных номеров и контактов
    if chosen_language == 'en':
        numbers = text(bold('Admissions Committee: '),
                       '\n+7 (495) 223-05-23 ',
                       '\n+7 (495) 276-37-37 ',
                       '\n8 (800) 550-91-42 ',
                       bold('\n\nMultifunctional Center: '),
                       '\n+7 (495) 223-05-23 ',
                       italic('\nExtension numbers: '),
                       '\nRECTOR’S OFFICE – Chief of rector’s office – Sholokhov Oleg Viktorovich: 1102 ',
                       '\nVICE-RECTOR FOR INTERNATIONAL ACTIVITIES – Assistant to the vice-rector – Gladyshova Irina Yuryevna: 1020 ',
                       '\nVICE-RECTOR FOR EDUCATIONAL AND SOCIAL WORK – Assistant to the vice-rector – Mazikina Irina Igorevna: 1272 ',
                       '\nMOBILIZATION DEPARTMENT – Department head – Kolesnikov Valeriy Alexeevich: 1025 ',
                       '\nADMISSIONS COMMITTEE – general number: 1640 ', )
    elif chosen_language == 'es':
        numbers = text(bold('Comité de Admisiones: '),
                       '\n+7 (495) 223-05-23 ',
                       '\n+7 (495) 276-37-37 ',
                       '\n8 (800) 550-91-42 ',
                       bold('\n\nCentro Multifuncional: '),
                       '\n+7 (495) 223-05-23 ',
                       italic('\nNúmeros de extensión: '),
                       '\nOFICINA DEL RECTOR-Jefe de la oficina del rector-Sholokhov Oleg Viktorovich: 1102 ',
                       '\nVICERRECTORA DE ACTIVIDADES INTERNACIONALES-Asistente de la vicerrectora-Gladyshova Irina Yuryevna: 1020 ',
                       '\nVICERRECTORA DE EDUCACIÓN Y TRABAJO SOCIAL-Asistente del vicerrector-Mazikina Irina Igorevna: 1272 ',
                       '\nDEPARTAMENTO DE MOVILIZACIÓN-Jefe de departamento-Kolesnikov Valeriy Alexeevich: 1025 ',
                       '\nCOMITÉ DE ADMISIONES-número general: 1640 ', )
    elif chosen_language == 'ar':
        numbers = text(bold('لجنة القبول: '),
                       '\n+7 (495) 223-05-23 ',
                       '\n+7 (495) 276-37-37 ',
                       '\n8 (800) 550-91-42 ',
                       bold('\n\nالمركز متعدد الوظائف: '),
                       '\n+7 (495) 223-05-23 ',
                       italic('\nأرقام التحويل: '),
                       '\nمكتب الرئيس - شولوخوف أوليج فيكتوروفيتش: 1102 ',
                       '\nنائب الرئيس للشؤون الدولية - مساعد نائب الرئيس - جلاديشوفا إرينا يوريفنا: 1020 ',
                       '\nنائب الرئيس للشؤون التعليمية والاجتماعية - مساعد نائب الرئيس - مازيكينا إرينا إيغوريفنا: 1272 ',
                       '\nقسم التعبئة والإحتراز - رئيس القسم - كوليسنيكوف فاليري أليكسيفيتش: 1025 ',
                       '\nلجنة القبول - الرقم العام: 1640 ', )
    else:
        numbers = text(bold('Приёмная комиссия: '),
                       '\n+7 (495) 223-05-23 ',
                       '\n+7 (495) 276-37-37 ',
                       '\n8 (800) 550-91-42 ',
                       bold('\n\nМногофункциональный центр: '),
                       '\n+7 (495) 223-05-23 ',
                       italic('\nДобавочные номера: '),
                       '\nАППАРАТ РЕКТОРА - Руководитель аппарата ректора - Шолохов Олег Викторович : 1102 ',
                       '\nПРОРЕКТОР ПО МЕЖДУНАРОДНОЙ ДЕЯТЕЛЬНОСТИ - Помощник проректора - Гладышева Ирина Юрьевна : 1020 ',
                       '\nПРОРЕКТОР ПО ВОСПИТАТЕЛЬНОЙ И СОЦИАЛЬНОЙ РАБОТЕ - Помощник проректора - Мазикина Ирина Игоревна : 1272 ',
                       '\nМОБИЛИЗАЦИОННЫЙ ОТДЕЛ - Начальник отдела - Колесников Валерий Алексеевич : 1025 ',
                       '\nПРИЕМНАЯ КОМИССИЯ - общий номер : 1640 ', )  # Если указан неверный язык, используем русский

    # Отправка сообщения с номерами телефонов и контактами
    await bot.send_message(callback_query.message.chat.id, numbers, parse_mode="MARKDOWN")
    await callback_query.answer()


# Обработчик нажатия кнопки "К корпусам"
@dp.callback_query_handler(lambda x: x.data and x.data in ['К корпусам', 'Student body', 'Cuerpo de estudiantes'])
async def academic_buildings(callback_query: types.CallbackQuery, state: FSMContext):
    # Получаем текущий язык из состояния
    data = await state.get_data()
    chosen_language = data.get('chosen_language', 'ru')  # Если язык не выбран, используем русский
    # Список адресов учебных корпусов
    if chosen_language == 'en':
        acbuilds = text(
            bold("The address of the campus on Bolshaya Semyonovskaya street: «Н»"),
            "\nacademic buildings «A», «B», «C», «N», «ND» ",
            "\nmetro station «Elektrozavodskaya» or railway station Elektrozavodskaya, B. Semyonovskaya str., 38. ",
            bold("\n\nThe address of the educational building at the Avtozavodskaya metro station: "),
            "\n115280, Moscow, Avtozavodskaya str., 16 (Avtozavodskaya metro station). ",
            bold("\n\nThe address of the educational building at the VDNKh metro station: "),
            "\nPavel Korchagin str., 22. ",
            bold("\n\nThe address of the educational building on Pryanishnikova Street: "),
            "\n127550, Moscow, Pryanishnikova str., 2A Buildings 1, 2 ",
            bold("\n\nThe address of the educational building on Mikhalkovskaya Street: "),
            "\n125493, Moscow, Mikhalkovskaya str., 7 ",
            bold("\n\nThe address of the academic building on Sadovaya-Spasskaya Street: "),
            "\n07045, Moscow, Sadovaya-Spasskaya str., 6 (Sukharevskaya metro station) ",
            bold("\n\nThe address of the educational building at the Aviamotornaya metro station: "),
            "\n111250, Lefortovsky Val str., Moscow, 111250 (Aviamotornaya metro station) ",
            bold("\n\nThe address of the educational building «D» and dormitory No. 3: "),
            "\nmetro station «Dubrovka», 1-ya Dubrovskaya str., 16a ",
        )
    elif chosen_language == 'es':
        acbuilds = text(
            bold("La dirección del campus en la calle Bolshaya Semyonovskaya: "),
            "\nedificios académicos «A», «B», «C», «N», «ND» ",
            "\nestación de metro «Elektrozavodskaya» o estación de tren Elektrozavodskaya, B. Semyonovskaya str., 38. ",
            bold("\n\nLa dirección del edificio educativo en la estación de metro Avtozavodskaya: "),
            "\n115280, Moscú, Avtozavodskaya str., 16 (estación de metro Avtozavodskaya). ",
            bold("\n\nLa dirección del edificio educativo en la estación de metro VDNKh: "),
            "\nPavel Korchagin str., 22. ",
            bold("\n\nLa dirección del edificio educativo en la calle Pryanishnikova: "),
            "\n127550, Moscú, calle Pryanishnikova., 2A Edificios 1, 2 ",
            bold("\n\nLa dirección del edificio educativo en la calle Mikhalkovskaya: "),
            "\n125493, Moscú, calle Mikhalkovskaya., 7 ",
            bold("\n\nLa dirección del edificio académico en la calle Sadovaya-Spasskaya: "),
            "\n07045, Moscú, calle Sadovaya-Spasskaya., 6 (Estación de metro Sukharevskaya) ",
            bold("\n\nLa dirección del edificio educativo en la estación de metro Aviamotornaya: "),
            "\nCalle Lefortovsky Val, 26., Moscú, 111250 (estación de metro Aviamotornaya) ",
            bold("\n\nLa dirección del edificio educativo « D  y dormitorio No. 3: "),
            "\nestación de metro «Dubrovka», 1-ya Dubrovskaya str., 16a ",
        )
    elif chosen_language == 'ar':
        acbuilds = text(
            bold("عنوان الحرم الجامعي على شارع بولشايا سيميونوفسكايا: "),
            "\n«مباني أكاديمية «أ»، «ب»، «ج»، »إن»، »إن دي ",
            "\nمحطة المترو «إليكتروزافودسكايا» أو محطة السكك الحديدية إليكتروزافودسكايا، شارع ب. سيميونوفسكايا، 38. ",
            bold("\n\nعنوان المبنى التعليمي في محطة مترو أفتوزافودسكايا: "),
            "\n115280، موسكو، شارع أفتوزافودسكايا، 16 (محطة مترو أفتوزافودسكايا). ",
            bold("\n\nعنوان المبنى التعليمي في محطة مترو في دي إن خ: "),
            "\n.شارع بافيل كورتشاجين، 22",
            bold("\n\n :عنوان المبنى التعليمي في شارع بريانيشنيكوفا"),
            "\n. 127550، موسكو، شارع بريانيشنيكوفا، 2أ، المباني 1، 2,",
            bold("\n\nعنوان المبنى التعليمي في شارع ميخالكوفسكايا: "),
            "\n125493، موسكو، شارع ميخالكوفسكايا، 7. ",
            bold("\n\nعنوان المبنى الأكاديمي في شارع سادوفايا سباسكايا: "),
            "\n07045، موسكو، شارع سادوفايا سباسكايا، 6 (محطة مترو سوخاريفسكايا). ",
            bold("\n\nعنوان المبنى التعليمي في محطة مترو أفياموتورنايا: "),
            "\n26 شارع ليفورتوفسكي فال، موسكو، 111250 (محطة مترو أفياموتورنايا). ",
            bold("\n\n:عنوان المبنى التعليمي «دي» والسكن الطلابي رقم 3"),
            "\n•	محطة المترو «دوبروفكا»، شارع دوبروفسكايا الأولى، 16أ. ",
        )
    else:
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
