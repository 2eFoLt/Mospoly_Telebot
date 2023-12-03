from .db_config import db_conf
import mysql.connector


def sql_start():
    global base, cur
    base = mysql.connector.connect(**db_conf)
    cur = base.cursor()
    if base:
        print('Data base connected OK!')


def get_questions():
    query = cur.execute("SELECT idquestions_ru, questions_ru FROM questions_ru")
    return query


def get_answers(idanswers_ru):
    query = cur.execute(f"SELECT answers_ru FROM 'answers_ru' WHERE idanswers_ru = {idanswers_ru}")
    return query
