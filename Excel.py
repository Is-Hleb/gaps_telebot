import xlsxwriter as excel
import PersonModel
import os
import datetime as dt


def gaps_on_date_file(month, year):
    data = []
    persons = PersonModel.load_all_persons()

    for i in range(1, 31):
        marked_persons = PersonModel.load_marked_on(i, month, year, False)
        for person in marked_persons:
            if persons.count(person) == 0:
                persons.append(person)

    path = f"cash/{month}-{year}.xlsx"

    try:
        os.mkdir("cash")
    except OSError as e:
        print(e.args)

    if month != dt.date.today().month or year != dt.date.today().year:
        try:
            return open(path, "rb")
        except Exception as e:
            print(e.args)

    wb = excel.Workbook(path)
    cell_format = wb.add_format()
    cell_format.set_border()

    ws = wb.add_worksheet("main")
    ws.set_column(0, 1, 2)
    ws.set_column(1, 2, 40)
    ws.set_column(2, 33, 5)
    ws.set_column(33, 34, 15)

    for i in range(0, len(persons) + 1):
        for j in range(0, 33):
            ws.write(i, j, "", cell_format)

    ws.write(0, 0, "№", wb.add_format().text_v_align)
    ws.write(0, 1, "ФИО", wb.add_format().text_v_align)

    ws.write(0, 33, "Уважительно", cell_format)
    ws.write(0, 34, "Неуважительно", cell_format)
    ws.write(0, 35, "Всего", cell_format)

    for i in range(1, 32):
        data.append(PersonModel.load_marked_on(i, month, year))
        ws.write(0, i + 1, i, cell_format)

    for i in range(0, len(persons)):
        ws.write(i + 1, 0, i + 1, cell_format)
        ws.write(i + 1, 1, persons[i]["name"], cell_format)

    row_got_data = [{"valid": 0, "not_valid": 0} for i in range(1, len(persons) + 10)]
    iteration = 0
    for day in data:
        for sel_person in day:
            gap = PersonModel.load_user_gap(sel_person["id"], iteration + 1, month, year)
            index = 0
            for index in range(0, len(persons)):
                if persons[index]["id"] == sel_person["id"]:
                    break
            ws.write(index + 1, iteration + 2, f"{gap['hours']} {'н' if gap['valid'] == 0 else 'у'}", cell_format)
            if gap["valid"] == 1:
                row_got_data[index + 1]["valid"] += gap["hours"]
            else:
                row_got_data[index + 1]["not_valid"] += gap["hours"]
        iteration += 1

    for index in range(0, len(persons)):
        ws.write(index + 1, 33, row_got_data[index + 1]["valid"], cell_format)
        ws.write(index + 1, 34, row_got_data[index + 1]["not_valid"], cell_format)
        ws.write(index + 1, 35, row_got_data[index + 1]["not_valid"] + row_got_data[index + 1]["valid"], cell_format)

    valid_sum = 0
    not_valid_sum = 0
    for index in range(0, len(persons)):
        valid_sum += row_got_data[index + 1]["valid"]
        not_valid_sum += row_got_data[index + 1]["not_valid"]

    ws.write(len(persons) + 1, 32, "Всего:", cell_format)
    ws.write(len(persons) + 1, 33, valid_sum, cell_format)
    ws.write(len(persons) + 1, 34, not_valid_sum, cell_format)
    ws.write(len(persons) + 1, 35, not_valid_sum + valid_sum, cell_format)

    wb.close()
    file = open(path, "rb")
    return file
