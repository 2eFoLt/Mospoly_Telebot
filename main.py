from aiogram import types, executor
from create_bot import dp
from inline import keyboard


async def on_startup(_):
    print("Я запустился!")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Вот тебе несколько вариантов", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
