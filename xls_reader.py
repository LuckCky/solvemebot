import xlrd

rb = xlrd.open_workbook('q/q.xls', formatting_info=True)
sheet = rb.sheet_by_name('Данные')

for rownum in range(sheet.nrows):
    row = sheet.row_values(rownum)
    print(row)
    for c_el in row:
        print(c_el)
