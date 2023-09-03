from connect_db import session
from models import Student, Subject, Teacher, Grade, Group
from faker import Faker

if __name__ == '__main__':
    
    # Ініціалізація генератора випадкових даних Faker
    fake = Faker()

    # Створення груп
    groups = [Group(id=i, name=f'Group №{i}') for i in range(1, 3 + 1)]
    session.add_all(groups)
    session.commit()

    # Створення викладачів
    teachers = [Teacher(name=fake.name()) for _ in range(3, 6)]
    session.add_all(teachers)
    session.commit()

    # Створення предметів та призначення їх викладачам
    subjects = [Subject(name=fake.word(), teacher=teachers[i % 3]) for i in range(5, 13)]
    session.add_all(subjects)
    session.commit()

    # Створення студентів та їх оцінок
    students = [Student(name=fake.name(), group_id=(i//10) + 1) for i in range(0, 30)]
    for student in students:
        student.student_grade = [
            Grade(student=student, subject=subjects[i % 8], grade=fake.random_int(min=1, max=100))
            for i in range(20)
        ]

    session.add_all(students)
    session.commit()