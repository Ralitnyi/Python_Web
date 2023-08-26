SELECT DISTINCT stud.name, s.subject
FROM subjects s
JOIN grades g ON s.subject_id = g.subject_id
JOIN students stud ON g.student_id = stud.id
WHERE stud.name = 'Jonathan Turner';
