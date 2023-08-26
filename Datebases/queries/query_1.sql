SELECT s.id, s.name, AVG(g.grade) AS avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.name
ORDER BY avg_grade DESC
LIMIT 5;
