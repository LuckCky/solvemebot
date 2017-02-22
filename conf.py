# -*- coding: utf-8 -*-

# Bot's token. Obtain yours from https://telegram.me/botfather
# solvemebot. telegram.me/solvemebot
token = '323106771:AAFhvq7fGQNRVOqwGDmPH2MywuJHtklEr4Y'

# Your own chat id. Ask https://telegram.me/my_id_bot to tell you yours
admins_list = []

storage_name = 'games.db'

# SQL stuff here
create_table = ('CREATE TABLE games ( userID VARCHAR(50), date DATE, questionNum VARCHAR(10), '
                'questionText VARCHAR(2000), answers VARCHAR(1000), status VARCHAR(30) )')
insert_questions = ('INSERT INTO games ( userID, date, questionNum, questionText, answers, status )'
                    ' VALUES ( %s, %s, %s, %s, %s, %s )')
select_current_question = "SELECT * FROM games WHERE userID = %s AND status = 'Active' AND date = %s"
change_correct_answers = ("UPDATE games SET {} = ( %s ) WHERE userID = %s AND "
                          "status = 'Active' AND date = %s")
select_next_question = ("SELECT * FROM games WHERE userID = %s AND status = 'Next' "
                        "AND questionNum > %s AND date = %s")
set_next_question = ("UPDATE games SET status = %s WHERE userID = %s "
                     "AND questionNum = %s AND date = %s")
select_all_questions = 'SELECT * FROM games WHERE userID = %s AND date = %s'
select_answered_questions = ("SELECT * FROM games WHERE userID = %s "
                             "AND status = 'Solved' AND date = %s")

# texts for messages here
greeting = 'Добро пожаловать в чертоги разума!  Вас ждет игра на сообразительность, в случае ' \
           'возникновения факапов и прочих багрепортов - пишите @gdeja'
not_welcome = 'Привет! Я бот для загадок. Часы работы с 21:00 до 23:00 МСК. Приходите позже.'
no_questions = 'Вопросов нет. Либо вы выиграли, либо что-то пошло не так'
right_answer = 'Правильный ответ! Вам осталось отгадать ещё {} ответ(-ов) на этот вопрос'
wrong_answer = ('Неправильный ответ, попробуйте переформулировать, '
                'переставить слова местами или дать другой ответ')
next_question = ('Переходим к следующему вопросу. Отправьте команду '
                 '/game, чтобы получить следующее задание')
change_answer = 'Переходим к следующему вопросу. На это вопрос вы сможете ответить позднее'
finished = 'Вы ответили правильно на все вопросы. Поздравляем!'
gone_wrong = 'Что-то пошло не так, попробуйте начать сначала или обратиться к администратору @gdeja'
game_score = 'Общее число вопросов: {0}. Из них решено: {1}.'

# xls with questions
questions_file = 'q/q.xls'
questions_sheet = 'Данные'
