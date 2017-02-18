import os
import datetime
import psycopg2
import urllib.parse

import xlrd

import conf

# urllib.parse.uses_netloc.append("postgres")
# for k, v in os.environ.items():
#     print(k, v)
# url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
# print(url)

import sqliter

def working_hours():
    d = datetime.datetime.now()
    if d.hour < 21 or d.hour >= 23:
        return False
    return True


def create_table():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    try:
        cursor = connection.cursor()
        cursor.execute(conf.create_table)
        connection.commit()
    except:
        pass
    finally:
        connection.close()
        return url


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
        return sqliter.SQLighter(conf.storage_name).select_next(user_id, 0)


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


def read_questions(statement, user_id):
    data = sqliter.SQLighter(conf.storage_name).select_any(statement, user_id)
    if data:
        return data
    else:
        pass
