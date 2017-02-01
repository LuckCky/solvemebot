import datetime
import sqlite3

import xlrd

import sqliter
import conf


def working_hours():
    d = datetime.datetime.now()
    if d.hour < 21 or d.hour >= 23:
        return False
    return True


def create_table():
    connection = sqlite3.connect(conf.storage_name)
    try:
        cursor = connection.cursor()
        cursor.execute(conf.create_table)
        connection.commit()
    except sqlite3.OperationalError:
        pass
    finally:
        connection.close()


def insert_questions(user_id):
    rb = xlrd.open_workbook(conf.questions_file, formatting_info=True)
    sheet = rb.sheet_by_name(conf.questions_sheet)

    connection = sqlite3.connect(conf.storage_name)
    cursor = connection.cursor()

    date = datetime.datetime.now().strftime('%Y-%m-%d')
    for rownum in range(1, sheet.nrows):
        row = sheet.row_values(rownum)
        correct_answers = row[-2].lower().split('\n')
        cursor.execute(conf.insert_questions, (user_id, date, row[0], row[1], row[2], row[3]))

        # if row[2].startswith('/'):
        # print('I GOT PIC HERE')
        # print(answers)
    connection.commit()


def read_current_question(user_id):
    current_string = sqliter.SQLighter(conf.storage_name).select_current(user_id)
    if current_string:
        return current_string
    else:
        return conf.no_questions


def read_next_question(user_id, question_num):
    next_string = sqliter.SQLighter(conf.storage_name).select_next(user_id, question_num)
    if next_string:
        return next_string
    else:
        return conf.no_questions


def change_correct_answers(user_id, value, column_name='answers'):
    rewrite_answers = sqliter.SQLighter(conf.storage_name).rewrite(
        client_id=user_id, col_name=column_name, val=value)
    if rewrite_answers:
        return True
    return False


def set_next_question(user_id, question_num, new_value, column_name):
    next_question_set = sqliter.SQLighter(conf.storage_name).rewrite(
        user_id, new_value, column_name, question_num)
    if next_question_set:
        return True
    return False
