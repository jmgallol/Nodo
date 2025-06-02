create database nodo;
use nodo;

CREATE TABLE Usuario (
documento_identidad INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
nombre_completo VARCHAR (255) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
genero VARCHAR(20) NOT NULL,
contraseña VARCHAR(255) NOT NULL,
telefono VARCHAR(20),
tipo INT CHECK (tipo IN (0, 1, 2)) -- 0: Administrador, 1: Profesor, 2: Estudiante
);


-- Tabla Profesor
CREATE TABLE Profesor (
    id_profesor INT NOT NULL  PRIMARY KEY,
	area_principal VARCHAR(50),
    area_alternativa VARCHAR(50),
    FOREIGN KEY (id_profesor)REFERENCES Usuario (documento_identidad)
);

-- Tabla Curso
CREATE TABLE Curso (
    id_curso INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(255),
    url_contenido VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    ano INT NOT NULL,
    semestre VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    profesor_asignado INT,
    FOREIGN KEY (profesor_asignado) REFERENCES Profesor(id_profesor)
);

-- Tabla Material
CREATE TABLE Material (
    id_material INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    nombre_archivo VARCHAR(255) NOT NULL,
    id_curso INT,
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
);

-- Tabla Tarea
CREATE TABLE Tarea (
    id_tarea INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    estado_entrega BOOLEAN,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_creacion DATE NOT NULL,
    fecha_entrega DATE NOT NULL,
    puntaje INT NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    id_curso INT,
    id_usuario INT,
    FOREIGN key (id_usuario) REFERENCES Usuario(documento_identidad),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
);

-- Tabla Foro
CREATE TABLE Foro (
    id_foro INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_creacion DATE NOT NULL,
    fecha_terminacion DATE,
    id_curso INT,
    id_profesor INT,
    FOREIGN KEY (id_profesor) REFERENCES Profesor(id_profesor),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
);

-- Tabla Mensaje
CREATE TABLE Mensaje (
    id_mensaje INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    id_foro INT,
    id_usuario INT,
    id_curso INT,
    mensaje_referencia INT,
    FOREIGN KEY (id_foro) REFERENCES Foro(id_foro),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(documento_identidad),
    FOREIGN KEY (mensaje_referencia) REFERENCES Mensaje(id_mensaje)
);

-- Tabla Matricula
CREATE TABLE Matricula (
    matricula_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_curso INT,
    id_usuario INT,
    confirmacionPago BOOLEAN NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(documento_identidad)
);