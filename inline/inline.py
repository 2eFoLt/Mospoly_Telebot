from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_category1 = InlineKeyboardButton('К вопросам', callback_data='К вопросам')
button_category2 = InlineKeyboardButton('К номерам', callback_data='К номерам')
button_category3 = InlineKeyboardButton('К корпусам', callback_data='К корпусам')
# button_category4 = InlineKeyboardButton('Назад', callback_data='Назад')

keyboard_main = InlineKeyboardMarkup(row_width=1)
keyboard_main.add(button_category1, button_category2, button_category3)

keyboard_questions = InlineKeyboardMarkup(row_width=1)
keyboard_questions.add(
    InlineKeyboardButton('Кто может подавать документы (родители, \nнесовершеннолетние школьники и т.д.)?', callback_data='q1'),
    InlineKeyboardButton('Есть ли в университете военная кафедра? Предоставляется ли отсрочка от армии?', callback_data='q2'),
    InlineKeyboardButton('Сколько мест для поступления по целевому обучению?', callback_data='q3'),
    InlineKeyboardButton('Как проходят внутренние экзамены?', callback_data='q4'),
    InlineKeyboardButton('Есть ли минимальный порог баллов за ЕГЭ и внутренние вступительные?', callback_data='q5'),
    InlineKeyboardButton('Есть ли образовательные программы на английском языке?', callback_data='q6'),
    InlineKeyboardButton('Можно ли подать апелляцию?', callback_data='q7'),
    InlineKeyboardButton('Что такое рейтинг? Что такое предварительный рейтинг и реальный рейтинг?', callback_data='q8'),
    InlineKeyboardButton('Как проходит обучение на заочной форме?', callback_data='q9'),
    InlineKeyboardButton('Предусмотрены ли скидки, отсрочки или рассрочки при поступлении на платную основу?', callback_data='q10'),
)
