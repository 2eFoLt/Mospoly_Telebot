from aiogram import types, executor
from create_bot import dp, bot
from inline import keyboard
from aiogram.utils.markdown import *


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
    await message.reply("Привет! Выбирайте нужный Вам раздел", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await message.delete()
    await message.answer(text=result)


@dp.callback_query_handler(lambda x: x.data and x.data in "К вопросам")
async def QandA(callback_query: types.CallbackQuery):
    questions = text(bold("Вопрос 1: "),
                     "\nОтвет: ",
                     bold("\n\nВопрос 2: "),
                     "\nОтвет: ",)

    await bot.send_message(callback_query.message.chat.id, questions, parse_mode="MARKDOWN")
    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
