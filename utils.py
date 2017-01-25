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


def create_questions_table(user_id):
    rb = xlrd.open_workbook(conf.questions_file, formatting_info=True)
    sheet = rb.sheet_by_name(conf.questions_sheet)

    connection = sqlite3.connect(conf.storage_name_params)
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
