from datetime import date

from sqlalchemy import desc, func

from connect_db import session
from models import Grade, Group, Student, Subject, Teacher


def select_1():
    return (
        session.query(
            Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


def select_2():
    subject_name = "maybe"
    return (
        session.query(
            Student.name, func.round(func.avg(Grade.grade)).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .group_by(Student.name)
        .order_by(desc("avg_grade"))
        .filter(Subject.name == subject_name)
        .limit(1)
        .all()
    )


def select_3():
    subject_name = "maybe"
    return (
        session.query(Group.name, func.round(func.avg(Grade.grade)))
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .group_by(Group.id)
        .all()
    )


def select_4():
    return session.query(func.round(func.avg(Grade.grade))).all()


def select_5():
    return (
        session.query(Teacher.name, Subject.name)
        .select_from(Subject)
        .join(Teacher)
        .order_by(Teacher.name)
        .all()
    )


def select_6():
    return (
        session.query(Group.name, Student.name)
        .select_from(Student)
        .join(Group)
        .order_by(Group.id)
        .all()
    )


def select_7():
    group_name = "Group №1"
    subject_name = "maybe"
    return (
        session.query(Group.name, Student.name, Grade.grade, Subject.name)
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .order_by(Group.id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )


def select_8():
    teacher_name = "Ryan Burnett"
    return (
        session.query(
            Teacher.name,
            Subject.name,
            func.round(func.avg(Grade.grade), 1).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .group_by(Teacher.name, Subject.name)
        .filter(Teacher.name == teacher_name)
        .all()
    )


def select_9():
    student_name = "Daniel Brown"
    return (
        session.query(Student.name, Subject.name)
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Student.name == student_name)
        .group_by(Subject.name, Student.name)
        .all()
    )


def select_10():
    student_name = "Daniel Brown"
    teacher_name = "Tammy Waller"
    return (
        session.query(Student.name, Subject.name)
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .group_by(Subject.name, Student.name)
        .all()
    )


def select_11():
    student_name = "Meagan Hodges"
    teacher_name = "Chelsea Sutton"
    return (
        session.query(func.round(func.avg(Grade.grade)), Teacher.name, Student.name)
        .select_from(Grade)
        .join(Subject)
        .join(Teacher)
        .join(Student)
        .group_by(Teacher, Student)
        .filter(Teacher.name == teacher_name, Student.name == student_name)
        .all()
    )


def select_12():
    subject_name = "Math"
    group_id = 1
    yesterday = date(date.today().year, date.today().month - 1, date.today().day)
    return (
        session.query(
            Grade.date,
            Grade.grade,
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Subject)
        .filter(
            Group.id == group_id, Subject.name == subject_name, Grade.date >= yesterday
        )
        .all()
    )


if __name__ == "__main__":
    for res in select_12():
        print(res)
