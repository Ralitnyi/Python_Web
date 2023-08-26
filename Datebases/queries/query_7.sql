SELECT g.grade, s.name, grp.name, sub.subject
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN groups grp ON s.group_id = grp.id
JOIN subjects sub ON g.subject_id = sub.subject_id
WHERE grp.name = 'Group A' AND sub.subject = 'Math';