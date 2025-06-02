# SI2003 – Sistemas de Gestión de Datos

**Estudiantes:**  
- David García Zapata
- Juan Manuel Gallo 

**Profesor:**  
- Edwin Nelson Montoya

---

## NODO – Sistema de Gestión de Datos

### 1. Descripción de la Actividad

Este proyecto corresponde a la implementación de un sistema de consola en Python para gestionar usuarios, cursos, matrículas, foros, materiales y tareas. El objetivo principal es que cada rol (Administrador, Profesor y Estudiante) pueda interactuar con la base de datos MySQL “nodo” mediante operaciones de CRUD básicas, autenticación y funcionalidades específicas según su tipo.

- **Administrador** puede:
  - Crear/consultar usuarios.
  - Matricular estudiantes en cursos.
  - Asignar profesores a cursos.
  - Visualizar reportes (cursos, información de cursos, listados de usuarios).

- **Profesor** puede:
  - Listar los cursos a los que fue asignado.
  - Ingresar a un curso y, dentro de él:
    - Listar alumnos matriculados.
    - Listar materiales (con título, descripción y nombre de archivo).
    - Visualizar y gestionar foros (enviar mensajes y responder).
    - Listar tareas asignadas.
    - Subir materiales (simulados como “nombre de archivo”).
    - Crear nuevos foros.

- **Estudiante** puede:
  - Listar los cursos en los cuales está matriculado.
  - Ingresar a un curso y, dentro de él:
    - Listar compañeros (alumnos matriculados).
    - Listar materiales disponibles.
    - Participar en los foros del curso (enviar mensajes y responder).
    - Listar tareas asignadas.
  
#### 1.1. Aspectos cumplidos / desarrollados
- Autenticación de usuarios (login/logout) mediante `username` y `password`.
- Roles de Usuario (0=Administrador, 1=Profesor, 2=Estudiante) con menús distintos.
- CRUD básico de Usuarios (creación, consulta).
- Matriculación de estudiantes y asignación de profesores.
- Funcionalidad completa para Profesor/Alumno (listar cursos, foros, materiales, tareas).
- Reportes para Administrador (filtrado de cursos y usuarios, vista detallada de curso).
- Persistencia en base de datos MySQL utilizando `mysql-connector-python`.

#### 1.2. Aspectos **NO** cumplidos / desarrollados
- Interfaz gráfica o aplicación web (solo consola de texto).
- Gestión de archivos reales en disco (los “materiales” se simulan únicamente con nombre).
- Control avanzado de permisos (todos los estudiantes/profesores ven los mismos datos de sus cursos, sin validaciones extras).
- Manejo de excepciones detalladas para todos los posibles errores de conexión.
- Pruebas unitarias o de integración automatizadas (solo pruebas manuales de consola).

---

### 2. Diseño de Alto Nivel

- **Arquitectura en Python**:  
  - `nodo.py` contiene todas las funciones y menús de la aplicación.
  - Cada menú (Administrador, Profesor/Alumno) invoca funciones que interactúan directamente con MySQL.

- **Patrones y Mejores Prácticas**:  
  - **Modularización**: se separaron las funciones de “Administración”, “Profesores/Alumnos” y “Reportes” en distintas responsabilidades.  
  - **Reutilización de la Conexión**: la función `conectar()` devuelve siempre un objeto de conexión nuevo, y cada función cierra la conexión al finalizar.  
  - **Transacciones**: en las operaciones críticas (p. ej. creación de usuario, matriculación, asignación de profesor), se usa `conn.start_transaction()` y `conn.commit()` / `conn.rollback()` para garantizar atomicidad.

- **Flujo de Datos**:  
  1. **Login** → verificación de credenciales en tabla `Usuario`.  
  2. Dependiendo de `tipo`:
     - **Tipo 0 (Admin)** → `menu_administrador()`  
     - **Tipo 1 o 2 (Profesor/Alumno)** → `menu_profesor_alumno()`

---

### 3. Ambiente de Desarrollo y Aspectos Técnicos

- **Lenguaje de Programación**:  
  - Python 3.8+ (probado en Python 3.10).

- **Librerías / Paquetes**:  
  - `mysql-connector-python` 
  - `datetime` (módulo estándar de Python)

- **Servidor de Base de Datos**:  
  - MySQL 
----

#### 3.1. Preparación del Entorno

1. **Instalar Python**  
   - Descargar e instalar Python 3.8+ desde [python.org](https://www.python.org/downloads/).  
   - En Windows, marcar “Add Python to PATH” durante la instalación.

2. **Instalar MySQL Server**  
   - Instalar MySQL Community Server 8.x (o 5.7).
   - Configuracion de la conexion del codigo python con la base de datos:
     - **host:** Poner el nombre del host que tenga la maquina desde la cual se va a ejectutar el programa, en nuestro caso es 'localhost' .
     - **user:** Entrar a la base de datos y mirar con que user tenemos nuestra base de datos y lo colacos en la parte del codigo que dice usea, en nuestro caso es 'user'.
     - **password:** Poner en el codigo de python la contraseña con la que tenemos configurada nuestra base de datos.
     - **database:** En este apartado dejamos ese nombre asi como esta ya que ese es el nombre de la base de datos con la cual vamos a trabajar nuestro programa.
     - **port:** En port vamos a poner el puerto de nuestra conexion de la base de datos, por lo general viene configurado como '3306'.

3. **Instalar `mysql-connector-python`**  
   ```bash
   pip install mysql-connector-python
