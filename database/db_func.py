from .db_config import db_conf
import mysql.connector


def sql_start():
    global base, cur
    base = mysql.connector.connect(**db_conf)
    cur = base.cursor()
    if base:
        print('Database connected OK!')


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
