SELECT s.subject, t.name
FROM subjects s
JOIN teachers t ON s.professor_id = t.id;
