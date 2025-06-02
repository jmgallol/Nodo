-- Insertar Administradores (tipo 0)
INSERT INTO Usuario (nombre_completo, email, genero, contraseña, telefono, tipo)
VALUES
( 'Pedro Gómez', 'pedro.gomez@eafit.edu.co', 'Masculino', 'nodo4', '3101234567', 0),
( 'Marta Díaz', 'marta.diaz@eafit.edu.co', 'Femenino', 'nodo5', '3102345678', 0),
( 'Luis Herrera', 'luis.herrera@eafit.edu.co', 'Masculino', 'nodo6', '3103456789', 0);

-- Insertar Profesores (tipo 1)
INSERT INTO Usuario ( nombre_completo, email, genero, contraseña, telefono, tipo)
VALUES
( 'Ana Torres', 'ana.torres@eafit.edu.co', 'Femenino', 'nodo1', '3001234567', 1),
( 'Carlos Ríos', 'carlos.rios@eafit.edu.co', 'Masculino', 'nodo2', '3002345678', 1),
( 'Laura Peña', 'laura.pena@eafit.edu.co', 'Femenino', 'nodo3', '3003456789', 1);

-- Insertar Estudiantes (tipo 2)
INSERT INTO Usuario ( nombre_completo, email, genero, contraseña, telefono, tipo)
VALUES
( 'Juan Pérez', 'juan.perez@eafit.edu.co', 'Masculino', 'nodo7', '3111234567', 2),
( 'Sofía Martínez', 'sofia.martinez@eafit.edu.co', 'Femenino', 'nodo8', '3112345678', 2),
( 'Diego Ramírez', 'diego.ramirez@eafit.edu.co', 'Masculino', 'nodo9', '3113456789', 2);

-- Insertar en la tabla Profesor
INSERT INTO Profesor (id_profesor, area_principal, area_alternativa)
VALUES
(4, 'Matemáticas', 'Física'),
(5,'Programación', 'Bases de Datos'),
(6, 'Literatura', 'Historia');



INSERT INTO Curso (nombre, categoria, url_contenido, fecha_inicio, fecha_fin, ano, semestre, precio, profesor_asignado)
VALUES
( 'Matemáticas Básicas', 'Ciencias', 'http://cursos.com/matematicas', '2025-02-01', '2025-06-30', 2025, '1', 100000.00, 4),
( 'Programación I', 'Tecnología', 'http://cursos.com/programacion1', '2025-02-01', '2025-06-30', 2025, '1', 150000.00, 5),
( 'Literatura Universal', 'Humanidades', 'http://cursos.com/literatura', '2025-02-01', '2025-06-30', 2025, '1', 120000.00, 6);


-- Insertar Materiales 
INSERT INTO Material ( titulo, descripcion, nombre_archivo, id_curso)
VALUES
( 'Álgebra Básica', 'Material introductorio de álgebra', 'algebra.pdf', 1),
( 'Variables en C', 'Guía sobre tipos de variables', 'variables.pdf', 2),
( 'Autores Clásicos', 'Resumen de autores antiguos', 'autores.pdf', 3);

-- Insertar Tareas 
INSERT INTO Tarea ( estado_entrega, nombre, descripcion, fecha_creacion, fecha_entrega, puntaje, nombre_archivo, id_curso, id_usuario)
VALUES
( TRUE, 'Tarea 1', 'Resolver ecuaciones', '2025-02-10', '2025-02-17', 100, 'ecuaciones.pdf', 1, 7),
( FALSE, 'Tarea 2', 'Escribir programa en C', '2025-02-11', '2025-02-20', 100, 'programa.c', 2, 8),
( TRUE, 'Tarea 3', 'Ensayo sobre Shakespeare', '2025-02-12', '2025-02-21', 100, 'ensayo.pdf', 3, 9);

-- Insertar Foros 
INSERT INTO Foro (nombre, descripcion, fecha_creacion, fecha_terminacion, id_curso, id_profesor)
VALUES
( 'Foro de Matemáticas', 'Discusión sobre problemas', '2025-02-05', '2025-06-01', 1, 4),
( 'Foro de C', 'Preguntas sobre sintaxis', '2025-02-06', '2025-06-01', 2, 5),
( 'Foro de Literatura', 'Interpretaciones de textos', '2025-02-07', NULL, 3, 6);


-- Insertar Mensajes 
INSERT INTO Mensaje ( nombre, descripcion, id_foro, id_usuario, id_curso, mensaje_referencia)
VALUES
( 'Pregunta 1', '¿Cómo se resuelve esta ecuación?', 1, 7, 1, NULL),
( 'Respuesta 1', 'Usa la fórmula cuadrática', 2, 4, 1, 1),
( 'Comentario', '¡Gracias por la respuesta!', 3, 7, 1, 2);

-- Insertar Matrículas 
INSERT INTO Matricula ( id_curso, id_usuario, confirmacionPago)
VALUES
( 1, 7, TRUE),
( 2, 8, TRUE),
( 3, 9, FALSE);




