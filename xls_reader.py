import xlrd

rb = xlrd.open_workbook('q/q.xls', formatting_info=True)
sheet = rb.sheet_by_name('Данные')

user_id = 1

import sqlite3

import conf

connection = sqlite3.connect(conf.storage_name_params)
cursor = connection.cursor()


for rownum in range(1, sheet.nrows):
    row = sheet.row_values(rownum)
    print(row)
    correct_answers = row[-2].lower().split('\n')
    cursor.execute(conf.insert_questions, (user_id, '2017-01-22', row[0], row[1], row[2], row[3]))

    # if row[2].startswith('/'):
        # print('I GOT PIC HERE')
    # print(answers)
print(correct_answers)
print(len(correct_answers))

if 'плющ плащ' in correct_answers:
    correct_answers.remove('плющ плащ')

print(correct_answers)
print(len(correct_answers))
connection.commit()
