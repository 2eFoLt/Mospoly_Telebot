# Импорт необходимых модулей и объектов
from .db_config import db_conf, db_conf_log
import mysql.connector


# Функция для подключения к базам данных
def sql_start():
    global base, cur, base_log, cur_log
    base = mysql.connector.connect(**db_conf)  # Установка соединения с базой данных вопросов
    cur = base.cursor()  # Создание объекта-курсора для выполнения SQL-запросов (вопросы)
    # Подключение к базе данных для журналирования
    base_log = mysql.connector.connect(**db_conf_log)  # Установка соединения с базой данных для логирования
    cur_log = base_log.cursor()  # Создание объекта-курсора для выполнения SQL-запросов (логирование)
    # Проверка успешности подключения к базе данных вопросов
    if base:
        print('Database connected OK!')
    # Проверка успешности подключения к базе данных логирования
    if base_log:
        print('Log Database connected OK!')


# Функция для получения вопросов из базы данных по заданному языку
def get_questions(language):
    table_name = f"questions_{language}"  # Формирование имени таблицы вопросов на заданном языке
    query = f"SELECT idquestions_{language}, questions_{language} FROM {table_name}"  # Формирование SQL-запроса
    cur.execute(query)  # Выполнение SQL-запроса
    questions = cur.fetchall() if cur else []  # Получение результатов запроса
    return questions  # Возврат списка вопросов


# Функция для получения ответов на заданный вопрос из базы данных по заданному языку
def get_answers(question_id, language):
    table_name = f"answers_{language}"  # Формирование имени таблицы ответов на заданном языке
    query = f"SELECT answers_{language} FROM {table_name} WHERE idanswers_{language} = {question_id}"  # Формирование SQL-запроса
    cur.execute(query)  # Выполнение SQL-запроса
    answers = cur.fetchall() if cur else []  # Получение результатов запроса
    return answers  # Возврат списка ответов


# Функция для записи данных о пользователе в журнал
def entry_user_id(sql_query, data):
    # Проверка существования пользователя в таблице логов
    sql_check_query = "SELECT login FROM logs WHERE login = %s"
    cur_log.execute(sql_check_query, data)  # Выполнение запроса на проверку существования пользователя
    result = cur_log.fetchone()  # Получение результата проверки
    # Если пользователя нет в таблице логов, выполняется вставка
    if not result:
        try:
            if data:
                cur_log.execute(sql_query, data)  # Вставка данных о пользователе в таблицу логов
            else:
                cur_log.execute(sql_query)  # Вставка данных о пользователе в таблицу логов без параметров
            base_log.commit()  # Фиксация изменений в базе данных
        except mysql.connector.Error as err:
            print(f"Error: {err}")  # Обработка возможной ошибки при выполнении запроса
