from db_config import db_config
import mysql.connector


def sql_start():
    global base, cur
    base = mysql.connector.connect(**db_config)
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.commit()


def get_questions():
    query = "SELECT idquestions_ru, questions_ru FROM questions_ru"
    return query


def get_answers(idanswers_ru):
    query = f"SELECT answers_ru FROM answers_ru WHERE idanswers_ru = {idanswers_ru}"
    return query


# @dp.callback_query_handler(lambda x: x.data and x.data == "К вопросам")
# async def show_questions(callback_query: types.CallbackQuery):
#     questions = get_questions()
#
#     keyboard_questions = types.InlineKeyboardMarkup(row_width=1)
#     for question_id, question_text in questions:
#         keyboard_questions.add(types.InlineKeyboardButton(text=question_text, callback_data=f"question:{question_id}"))
#
#     await bot.send_message(callback_query.message.chat.id, text='Список вопросов:', reply_markup=keyboard_questions)
#     await callback_query.answer()
#
#
# @dp.callback_query_handler(lambda x: x.data and x.data.startswith("question:"))
# async def show_answers(callback_query: types.CallbackQuery):
#     question_id = int(callback_query.data.split(":")[1])
#
#     answers = get_answers(question_id)
#
#     answer_text = "\n".join(answer for (answer,) in answers)
#     await bot.send_message(callback_query.message.chat.id, text=f'Ответ на вопрос {answer_text}')
#     await callback_query.answer()
