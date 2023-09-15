from datetime import datetime

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    student_grade = relationship("Grade", back_populates="student")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subjects_taught = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects_taught")
    subject_grade = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="student_grade")
    grade = Column(Integer)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    date = Column(Date, default=datetime.now())
    subject = relationship("Subject", back_populates="subject_grade")
