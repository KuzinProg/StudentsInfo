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
            "INSERT INTO student (first_name, last_name, middle_name, gender, birth_date, phone, address, "
            "average_mark, stud_group, photo) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (student.first_name, student.last_name, student.middle_name, student.gender,
             student.birth_date, student.phone, student.address,
             str(student.average_mark), student.group, student.photo))
        DataBase.connection.commit()

    @staticmethod
    def get_students(group=None):
        group_filter = f'WHERE student.stud_group = {group}'
        cursor = DataBase.connection.cursor()
        cursor.execute(
            "SELECT student.id, first_name, last_name, middle_name, gender, photo, birth_date, phone, "
            "address, name, average_mark FROM student "
            "INNER JOIN stud_group "
            "ON student.stud_group = stud_group.id "
            f"{group_filter if group is not None else ''}")
        result = cursor.fetchall()
        students = []
        for item in result:
            students.append(Student(*item))
        cursor.close()
        return students

    @staticmethod
    def get_student(id):
        cursor = DataBase.connection.cursor()
        cursor.execute(
            "SELECT student.id, first_name, last_name, middle_name, gender, photo, birth_date, phone, "
            "address, name, average_mark FROM student "
            "INNER JOIN stud_group "
            "ON student.stud_group = stud_group.id "
            "WHERE student.id=?", (id,))
        result = cursor.fetchone()
        if result is None:
            return None
        cursor.close()
        return Student(*result)


    def get_id_group(self, group_name):
        cursor = DataBase.connection.cursor()
        cursor.execute(
            "SELECT id FROM stud_group "
            "WHERE name=?", (group_name,))
        result = cursor.fetchone()
        if result is None:
            return None
        cursor.close()
        return result[0]


    @staticmethod
    def update_student(student: Student):
        group_id = DataBase.get_id_group(student.group)
        cursor = DataBase.connection.cursor()
        cursor.execute("UPDATE student SET first_name = ?, last_name = ?, middle_name = ?, gender = ?, photo = ?, "
                       "birth_date = ?, phone = ?, address = ?, stud_group = ?, average_mark = ? "
                       "WHERE id=?", (student.first_name, student.last_name, student.middle_name, student.gender,
                                      student.photo, student.birth_date, student.phone, student.address, group_id,
                                      student.average_mark, student.id))
        DataBase.connection.commit()
        cursor.close()


    @staticmethod
    def get_groups():
        cursor = DataBase.connection.cursor()
        cursor.execute("SELECT * FROM stud_group")
        result = cursor.fetchall()
        cursor.close()
        return result
