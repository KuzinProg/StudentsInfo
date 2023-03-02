import sqlite3

from student import Student


class DataBase:
    connection = sqlite3.connect('studentsinfo_db.db')

    @staticmethod
    def get_user(login: str, password: str):
        cursor = DataBase.connection.cursor()
        cursor.execute("SELECT role FROM user "
                       "WHERE login=? AND password=?", (login, password))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result is not None else None

    @staticmethod
    def add_student(student: Student):
        cursor = DataBase.connection.cursor()
        cursor.execute(
            "INSERT INTO student (first_name, last_name, middle_name, gender, birth_date, phone, address, average_mark, stud_group) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (student.first_name, student.last_name, student.middle_name, student.gender,
                                                student.birth_date, student.phone, student.address,
                                                str(student.average_mark), student.group))
        DataBase.connection.commit()

    @staticmethod
    def get_students():
        cursor = DataBase.connection.cursor()
        cursor.execute("SELECT * FROM student")
        result = cursor.fetchall()
        cursor.close()
        return result

    @staticmethod
    def get_groups():
        cursor = DataBase.connection.cursor()
        cursor.execute("SELECT * FROM stud_group")
        result = cursor.fetchall()
        cursor.close()
        return result
