from .db_config import db_conf, db_conf_log
import mysql.connector


def sql_start():
    global base, cur, base_log, cur_log
    base = mysql.connector.connect(**db_conf)
    cur = base.cursor()
    base_log = mysql.connector.connect(**db_conf_log)
    cur_log = base_log.cursor()
    if base:
        print('Database connected OK!')
    if base_log:
        print('Log Database connected OK!')


def get_questions(language):
    table_name = f"questions_{language}"
    query = f"SELECT idquestions_{language}, questions_{language} FROM {table_name}"
    cur.execute(query)
    questions = cur.fetchall() if cur else []
    return questions


def get_answers(question_id, language):
    table_name = f"answers_{language}"
    query = f"SELECT answers_{language} FROM {table_name} WHERE idanswers_{language} = {question_id}"
    cur.execute(query)
    answers = cur.fetchall() if cur else []
    return answers

def entry_user_id(sql_query, data):
    # Проверяем, существует ли уже user_id в таблице
    sql_check_query = "SELECT login FROM logs WHERE login = %s"
    cur_log.execute(sql_check_query, data)
    result = cur_log.fetchone()
    # Если user_id не существует, то выполняем вставку
    if not result:
        try:
            if data:
                cur_log.execute(sql_query, data)
            else:
                cur_log.execute(sql_query)
            base_log.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

