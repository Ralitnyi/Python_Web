-- Drop existing tables if they exist
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS students;

-- Table: students 
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

-- Table: groups 
CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Table: teachers
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Table: subjects
CREATE TABLE subjects(
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject VARCHAR(100) NOT NULL,
    professor_id INTEGER,
    FOREIGN KEY (professor_id) REFERENCES teachers(id)
);

-- Table: grades
CREATE TABLE grades(
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    grade INTEGER,
    grade_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

