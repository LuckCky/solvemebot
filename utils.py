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
    current_string = sqliter.SQLighter(conf.storage_name).select_single(user_id)
    if current_string:
        return current_string
    else:
        return conf.no_questions


def change_correct_answers(user_id, value, column_name='answers'):
    rewrite_answers = sqliter.SQLighter(conf.storage_name).rewrite(user_id, column_name, value)
    if rewrite_answers:
        return True
    return False
