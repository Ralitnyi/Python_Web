SELECT st.group_id, AVG(g.grade) AS avg_grade
FROM students st
JOIN grades g ON st.id = g.student_id
WHERE g.subject_id = subject_id
GROUP BY st.group_id;
