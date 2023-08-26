SELECT DISTINCT stud.name, s.subject, t.name
FROM subjects s
JOIN grades g ON s.subject_id = g.subject_id
JOIN students stud ON g.student_id = stud.id
JOIN teachers t ON s.professor_id = t.id
WHERE stud.name = 'Jonathan Turner';
