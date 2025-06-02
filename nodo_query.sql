
SELECT U.nombre_completo, M.matricula_id
FROM Usuario U
JOIN Matricula M ON U.documento_identidad = M.id_usuario
JOIN Curso C ON C.id_curso = M.id_curso
WHERE U.tipo = 2 AND C.ano = 2025 AND C.semestre = '1'
ORDER BY U.nombre_completo ASC;

SELECT DISTINCT U.nombre_completo
FROM Usuario U
JOIN Matricula M ON U.documento_identidad = M.id_usuario
JOIN Curso C ON C.id_curso = M.id_curso
WHERE U.tipo = 2 AND C.id_curso = 2 AND C.ano = 2025 AND C.semestre = '1';

SELECT C.nombre, C.fecha_inicio, C.fecha_fin
FROM Curso C
JOIN Matricula M ON C.id_curso = M.id_curso
WHERE M.id_usuario = 8 AND C.fecha_inicio BETWEEN '2025-01-01' AND '2025-12-31';

SELECT P.id_profesor, U.nombre_completo, C.nombre AS curso
FROM Profesor P
JOIN Usuario U ON P.id_profesor = U.documento_identidad
JOIN Curso C ON C.profesor_asignado = P.id_profesor
WHERE CURDATE() BETWEEN C.fecha_inicio AND C.fecha_fin;

SELECT nombre, categoria
FROM Curso
ORDER BY categoria ASC;

SELECT nombre, precio
FROM Curso
WHERE precio BETWEEN 100000 AND 500000;


SELECT U.nombre_completo
FROM Usuario U
WHERE U.tipo = 2 AND NOT EXISTS (
    SELECT 1
    FROM Matricula M
    JOIN Curso C ON C.id_curso = M.id_curso
    WHERE M.id_usuario = U.documento_identidad AND C.ano = 2025 AND C.semestre = '1'
);

SELECT nombre, categoria
FROM Curso
WHERE categoria = 'Tecnología';

SELECT nombre, descripcion, fecha_entrega
FROM Tarea
WHERE id_curso = 2;

SELECT M.titulo, M.descripcion, M.nombre_archivo
FROM Material M
JOIN Curso C ON M.id_curso = C.id_curso
WHERE C.id_curso = 3;

SELECT Msg.id_mensaje, U.nombre_completo AS remitente, Msg.nombre AS asunto
FROM Mensaje Msg
JOIN Usuario U ON Msg.id_usuario = U.documento_identidad
WHERE Msg.id_foro = 1;


SELECT C.nombre AS curso, COUNT(M.id_usuario) AS total_estudiantes
FROM Curso C
JOIN Matricula M ON C.id_curso = M.id_curso
WHERE C.ano = 2025 AND C.semestre = '1'
GROUP BY C.nombre;


