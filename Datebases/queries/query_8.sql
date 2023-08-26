SELECT AVG(g.grade) AS avg_grade, t.name AS teacher_name, s.subject
FROM grades g
JOIN subjects s ON g.subject_id = s.subject_id
JOIN teachers t ON s.professor_id = t.id
GROUP BY t.name, s.subject;