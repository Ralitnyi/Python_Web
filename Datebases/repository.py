import sqlite3
import random

from faker import Faker 

def create_db():
    with open('init_todo.sql', 'r') as f:
        sql = f.read()

    with sqlite3.connect('todo.db') as con:
        cur = con.cursor()
        cur.executescript(sql)


def populate_db():

    #table filling students
    students_sql_command = []
    group_id = 1
    for i in range(1, 31):
        if i > 10 and i < 21:
            group_id = 2
        elif i > 20:
            group_id = 3
        st_sql_command = f"INSERT INTO students (name, group_id) VALUES ('{Faker().name()}', {group_id});"
        students_sql_command.append(st_sql_command)

    students_sql_command = '\n'.join(students_sql_command)
    with sqlite3.connect('todo.db') as con:
        cur = con.cursor()
        cur.executescript(students_sql_command)
        # cur.execute("SELECT id from students;")
        # students_ids = [obj[0] for obj in cur.fetchall()]        
        # print(students_ids)

    #table filling groups
    groups_names = ["Group A", "Group B", "Group C"]
    #groups_len = len(groups_names)                      #########
    groups_sql_command = '\n'.join(f"INSERT INTO groups (name) VALUES ('{name}');" for name in groups_names)

    with sqlite3.connect('todo.db') as con:
        cur = con.cursor()
        cur.executescript(groups_sql_command)


    #table filling teachers

    teachers_sql_command = '\n'.join(f"INSERT INTO teachers (name) VALUES ('{Faker().name()}');" for _ in range(5))
    with sqlite3.connect('todo.db') as con:
        cur = con.cursor()
        cur.executescript(teachers_sql_command)

    #table filling subjects
    subjects = ["Math", "Physics", "Chemistry", "Biology", "History", "Literature", "Computer Science"]
    professors_ids = [1, 3, 2, 4, 5, 2, 1]

    subjects_sql_commands = []
    for subject, professor_id in zip(subjects, professors_ids):
        sql_command = f"INSERT INTO subjects (subject, professor_id) VALUES ('{subject}', {professor_id});"
        subjects_sql_commands.append(sql_command)

    # Об'єднання всіх SQL-команд у одному рядку
    all_sql_commands = '\n'.join(subjects_sql_commands)
    with sqlite3.connect('todo.db') as con:
        cur = con.cursor()
        cur.executescript(all_sql_commands)


    #table filling grades
    with sqlite3.connect('todo.db') as con:
        cur = con.cursor()

        # Отримання списку студентів
        cur.execute("SELECT id FROM students")
        student_ids = [row[0] for row in cur.fetchall()]

        # Вставка випадкових оцінок для кожного студента та предмета
        for student_id in student_ids:
            for subject_id in range(1, len(subjects) + 1):
                num_grades = random.randint(1, 6)  # Випадкова кількість оцінок
                for _ in range(num_grades):
                    grade = random.randint(1, 100)  # Випадкова оцінка
                    cur.execute(f"INSERT INTO grades (student_id, subject_id, grade) VALUES ({student_id}, {subject_id}, {grade});")

        # Збереження змін
        con.commit()



def query_db(query_file):

    with open(f'queries/{query_file}', 'r') as file:
        query = file.read()

    with sqlite3.connect('todo.db') as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result        