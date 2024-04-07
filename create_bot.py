# Импорт необходимых классов из модуля aiogram
from aiogram import Bot, Dispatcher
# Импорт токена бота из файла конфигурации
from config import TOKEN
# Импорт класса для хранения состояний FSM в памяти
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Создание объекта бота с использованием токена
bot = Bot(token=TOKEN)
# Создание объекта для хранения состояний FSM в памяти
storage = MemoryStorage()
# Создание диспетчера для обработки запросов от бота с использованием объекта бота и объекта хранения состояний
dp = Dispatcher(bot, storage=storage)
