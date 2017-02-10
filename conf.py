# -*- coding: utf-8 -*-

# Bot's token. Obtain yours from https://telegram.me/botfather
# solvemebot. telegram.me/solvemebot
token = '323106771:AAFhvq7fGQNRVOqwGDmPH2MywuJHtklEr4Y'

# Shelve database file name
storage_name = "messages"

# Your own chat id. Ask https://telegram.me/my_id_bot to tell you yours
admins_list = []

storage_name_params = 'games.db'

# SQL stuff here
create_table = ('CREATE TABLE games ( userID VARCHAR(50), date DATETIME (20), questionNum VARCHAR(10), '
                'questionText VARCHAR(2000), answers VARCHAR(1000), status VARCHAR(30) )')
insert_questions = ('INSERT INTO games ( userID, date, questionNum, questionText, answers, status )'
                    ' VALUES ( ?, ?, ?, ?, ?, ? )')

# texts for messages here
greeting = 'Привет! Я бот для загадок, а тут приветственный текст. Используйте команду /game чтобы начать игру '
not_welcome = 'Привет! Я бот для загадок. Часы работы с 21:00 до 23:00 МСК. Приходите позже.'

# xls stuff
questions_file = 'q/q.xls'
questions_sheet = 'Данные'
