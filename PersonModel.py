import sqlite3 as sql
import functions as Fun


def get_connection():
    return sql.connect("main.db", check_same_thread=False)


conn = get_connection()
with conn:
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS PERSON (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                deleted INTEGER DEFAULT 0
            );
    """)
    conn.commit()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS GAPS (
            person_id INTEGER,
            month INTEGER,
            day INTEGER,
            year INTEGER,
            hours INTEGER,
            valid INTEGER DEFAULT 1
        );
    """)
    conn.commit()


def delete_marked_on(day, month, year):
    query = """DELETE FROM GAPS WHERE day = ? AND month = ? AND year = ?"""
    cursor.execute(query, [day, month, year])
    conn.commit()


def delete_all_persons():
    cursor.execute("""UPDATE PERSON set DELETED = 1 WHERE DELETED = 0""")
    conn.commit()


def load_user_gap(index, day, month, year):
    query = """SELECT * FROM GAPS WHERE person_id = ? AND day = ? AND month = ? AND year = ?"""
    data = cursor.execute(query, [index, day, month, year])
    gap = {}
    for row in data:
        gap = {
            "person_id": row[0],
            "month": row[1],
            "day": row[2],
            "year": row[3],
            "hours": row[4],
            "valid": int(row[5]),
        }
        return gap


def load_marked_on(day, month, year, with_valid_star=True):
    try:
        query = """SELECT * FROM GAPS WHERE day = ? AND month = ? AND year = ?"""
        data = cursor.execute(query, [day, month, year])
        conn.commit()

        person_ids = []
        for row in data:
            person_ids.append(row[0])
        persons = []
        for index in person_ids:
            person = load_person_by_index(index, True)
            valid = load_user_gap(index, day, month, year)["valid"]
            persons.append({
                "name": person["name"] + ("*" if valid == 0 and with_valid_star else ""),
                "id": index,
                "deleted": person["deleted"]
            })
    except Exception as e:
        Fun.addToLog(e.args)
        return []
    return persons


def mark(index, year, month, day, valid, hours):
    query = """SELECT * FROM GAPS WHERE (PERSON_ID = ? AND YEAR = ? AND MONTH = ? AND DAY = ?)"""
    data = cursor.execute(query, [index, year, month, day])
    for row in data:
        if len(row) > 0:
            query = "UPDATE GAPS set VALID = ?, HOURS = ? WHERE PERSON_ID = ? AND YEAR = ? AND MONTH = ? AND DAY = ?"
            cursor.execute(query, [valid, hours, index, year, month, day])
            conn.commit()
            return

    query = """INSERT INTO GAPS (PERSON_ID, YEAR, MONTH, DAY, VALID, HOURS) VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, [index, year, month, day, valid, hours])
    conn.commit()


def add_in_list(name):
    cursor.execute("INSERT INTO PERSON (name) values (?)", [name])
    conn.commit()


def delete_by_arr_of_id(arr):
    query = "UPDATE PERSON set DELETED = 1 WHERE id IN ("
    for i in range(0, len(arr)):
        query += "?,"
    query = query[:-1] + ")"
    cursor.execute(query, arr)
    conn.commit()


def load_person_by_index(index, also_deleted=False):
    dataa = cursor.execute(f"SELECT * FROM PERSON WHERE ID = {index}" + ("AND DELETED = 0" if not also_deleted else ""))
    for data in dataa:
        return {
            "id": data[0],
            "name": data[1],
            "deleted": data[2],
        }


def load_all_persons():
    data = cursor.execute("""SELECT * FROM PERSON WHERE DELETED = 0""")
    out_data = []
    for row in data:
        out_data.append({
            "name": row[1],
            "id": row[0],
            "deleted": 0
        })
    return out_data


def load_all_names():
    data = cursor.execute("SELECT * FROM PERSON WHERE DELETED = 0")
    data_to_return = []
    for row in data:
        data_to_return.append({"name": row[1], "id": row[0]})
    return data_to_return


def get_all_dates():
    data = cursor.execute("""SELECT DISTINCT MONTH, YEAR FROM GAPS""")
    ret_data = []
    for row in data:
        ret_data.append({
            "month": int(row[0]),
            "year": int(row[1])
        })
    return ret_data
