from aiogram import types, executor
from create_bot import dp, bot
from inline import keyboard_main, keyboard_questions
from aiogram.utils.markdown import *
from answers import answers_database


async def on_startup(_):
    print("Я запустился!")


HELP_MESSAGE = """Данный бот является помощником для иностранных студентов
В разделе 'К вопросам' Вы список самых часто задаваемых вопросов и ответов к ним
В разделе 'К номерам' Вы можете найти список номеров, которые могут быть Вам полезны
В разделе 'К корпусам' Вы можете найти информацию о корпусах (где находится, важные кабинеты и другое)
Для начала работы с ботом пропишите команду /start
Если у вас возникли вопросы или проблемы, свяжитесь с нами по электронной почте xxx@example.com"""

my_list = HELP_MESSAGE.split('\n')

result = ""
for item in my_list:
    result += f"\u2022 {item}\n"


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Выбирайте нужный Вам раздел", reply_markup=keyboard_main)


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await message.delete()
    await message.answer(text=result)


@dp.callback_query_handler(lambda x: x.data and x.data in "К вопросам")
async def QandA(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.message.chat.id, text='Список вопросов:', reply_markup=keyboard_questions)
    await callback_query.answer()
    # questions = text(bold("Вопрос 1: "),
    #                  "\nОтвет: ",
    #                  bold("\n\nВопрос 2: "),
    #                  "\nОтвет: ", )
    #
    # await bot.send_message(callback_query.message.chat.id, questions, parse_mode="MARKDOWN")
    # await callback_query.answer()


@dp.callback_query_handler(lambda x: x.data.startswith('q'))
async def process_question(callback_query: types.CallbackQuery):
    question_number = callback_query.data[1:]

    answer = answers_database.get(question_number, 'Ответ не найден')

    await bot.send_message(callback_query.message.chat.id, f"Ответ: {answer}")
    await callback_query.answer()


# кнопка "К номерам"
@dp.callback_query_handler(lambda x: x.data and x.data in 'К номерам')
async def phone_numbers(callback_query: types.CallbackQuery):
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
                   '\nПРИЕМНАЯ КОМИССИЯ - общий номер : 1640 ', )

    await bot.send_message(callback_query.message.chat.id, numbers, parse_mode="MARKDOWN")
    await callback_query.answer()


# кнопка "К корпусам"
@dp.callback_query_handler(lambda x: x.data and x.data in 'К корпусам')
async def academic_buildings(callback_query: types.CallbackQuery):
    acbuilds = text(bold("Адрес кампуса на Большой Семёновской: "),
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
                    "\nст. м. «Дубровка», ул. 1-я Дубровская, д. 16а. ", )

    await bot.send_message(callback_query.message.chat.id, acbuilds, parse_mode="MARKDOWN")
    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
