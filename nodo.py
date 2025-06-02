import mysql.connector
from datetime import date

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2208",
        database="nodo",
        port="3306"
    )

def login():
    email = input("Correo electrónico: ")
    contraseña = input("Contraseña: ")
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Usuario WHERE email = %s AND contraseña = %s",
        (email, contraseña)
    )
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        print(f"\nBienvenido/a, {usuario['nombre_completo']} (Rol: {usuario['tipo']})")
        return usuario
    else:
        print("\nUsuario o contraseña incorrectos.")
        return None

# ─── Funciones de Administrador ───────────────────────────────────────────────

def crear_usuario():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("\n--- Crear nuevo usuario ---")
        nombre = input("Nombre completo: ")
        email = input("Email: ")
        genero = input("Género (Masculino/Femenino): ")
        contraseña = input("Contraseña: ")
        telefono = input("Teléfono: ")
        tipo = int(input("Tipo (0 = Admin, 1 = Profesor, 2 = Estudiante): "))
        conn.start_transaction()
        cursor.execute(
            """
            INSERT INTO Usuario
                (nombre_completo, email, genero, contraseña, telefono, tipo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nombre, email, genero, contraseña, telefono, tipo)
        )
        new_id = cursor.lastrowid
        if tipo == 1:
            area_principal = input("Área principal del profesor: ")
            area_alternativa = input("Área alternativa del profesor: ")
            cursor.execute(
                """
                INSERT INTO Profesor (id_profesor, area_principal, area_alternativa)
                VALUES (%s, %s, %s)
                """,
                (new_id, area_principal, area_alternativa)
            )
        conn.commit()
        print(f"Usuario creado correctamente con ID {new_id}.")
    except Exception as e:
        conn.rollback()
        print("Error al crear usuario:", e)
    finally:
        conn.close()

def ver_usuario():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        doc = int(input("Ingrese el documento del usuario a consultar: "))
        cursor.execute(
            "SELECT * FROM Usuario WHERE documento_identidad = %s",
            (doc,)
        )
        u = cursor.fetchone()
        if u:
            print("\nDatos del usuario:")
            for k,v in u.items():
                print(f"  {k}: {v}")
        else:
            print("No se encontró el usuario.")
    finally:
        conn.close()

def matricular_usuario():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("\n--- Matricular Usuario a Curso ---")
        id_usuario = int(input("ID del usuario (estudiante): "))
        id_curso   = int(input("ID del curso: "))
        conn.start_transaction()
        cursor.execute(
            "SELECT * FROM Usuario WHERE documento_identidad = %s AND tipo = 2",
            (id_usuario,)
        )
        if not cursor.fetchone():
            raise Exception("El usuario no existe o no es un estudiante.")
        cursor.execute(
            "SELECT * FROM Curso WHERE id_curso = %s",
            (id_curso,)
        )
        if not cursor.fetchone():
            raise Exception("El curso no existe.")
        cursor.execute(
            "SELECT * FROM Matricula WHERE id_usuario = %s AND id_curso = %s",
            (id_usuario, id_curso)
        )
        if cursor.fetchone():
            raise Exception("El estudiante ya está matriculado en este curso.")
        cursor.execute(
            "INSERT INTO Matricula (id_curso, id_usuario, confirmacionPago) VALUES (%s, %s, %s)",
            (id_curso, id_usuario, True)
        )
        conn.commit()
        print("Estudiante matriculado correctamente.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()

def ver_matricula():
    conn = conectar()
    cursor = conn.cursor()
    try:
        doc = int(input("Documento del estudiante: "))
        cursor.execute(
            """
            SELECT C.nombre, C.semestre, C.ano
            FROM Matricula M
            JOIN Curso C ON M.id_curso = C.id_curso
            WHERE M.id_usuario = %s
            """,
            (doc,)
        )
        rows = cursor.fetchall()
        if rows:
            print("\nEl estudiante está matriculado en:")
            for nombre, sem, ano in rows:
                print(f"  📘 {nombre} - Semestre {sem}-{ano}")
        else:
            print("El estudiante no está matriculado en ningún curso.")
    finally:
        conn.close()

def asignar_profesor():
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("\n--- Asignar Profesor a Curso ---")
        id_prof  = int(input("ID del profesor: "))
        id_curso = int(input("ID del curso: "))
        conn.start_transaction()
        cursor.execute(
            "SELECT * FROM Profesor WHERE id_profesor = %s",
            (id_prof,)
        )
        if not cursor.fetchone():
            raise Exception("El profesor no existe.")
        cursor.execute(
            "SELECT * FROM Curso WHERE id_curso = %s",
            (id_curso,)
        )
        if not cursor.fetchone():
            raise Exception("El curso no existe.")
        cursor.execute(
            "UPDATE Curso SET profesor_asignado = %s WHERE id_curso = %s",
            (id_prof, id_curso)
        )
        conn.commit()
        print("Profesor asignado correctamente al curso.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()

def menu_reportes():
    conn = conectar()
    cursor = conn.cursor()
    try:
        while True:
            print("\n--- MENÚ DE REPORTES ---")
            print("1. Listar cursos (por ID, profesor, fechas)")
            print("2. Ver información de un curso")
            print("3. Listar usuarios (por rol o ID)")
            print("4. Salir")
            opt = input("Opción: ")
            if opt == "1":
                filtro = input("Filtrar por (id/profesor/fecha/todos): ")
                if filtro == "id":
                    cid = int(input("ID del curso: "))
                    cursor.execute("SELECT * FROM Curso WHERE id_curso = %s", (cid,))
                elif filtro == "profesor":
                    pid = int(input("ID del profesor: "))
                    cursor.execute("SELECT * FROM Curso WHERE profesor_asignado = %s", (pid,))
                elif filtro == "fecha":
                    inicio = input("Desde (YYYY-MM-DD): ")
                    fin    = input("Hasta (YYYY-MM-DD): ")
                    cursor.execute(
                        "SELECT * FROM Curso WHERE fecha_inicio BETWEEN %s AND %s",
                        (inicio, fin)
                    )
                else:
                    cursor.execute("SELECT * FROM Curso")
                for row in cursor.fetchall():
                    print(row)

            elif opt == "2":
                cid = int(input("ID del curso: "))
                cursor.execute(
                    """
                    SELECT C.nombre, C.categoria, C.fecha_inicio, C.fecha_fin, U.nombre_completo
                    FROM Curso C
                    LEFT JOIN Usuario U ON C.profesor_asignado = U.documento_identidad
                    WHERE C.id_curso = %s
                    """,
                    (cid,)
                )
                curso = cursor.fetchone()
                if curso:
                    print(f"\nCurso: {curso[0]}")
                    print(f"Categoría: {curso[1]}")
                    print(f"Fechas: {curso[2]} a {curso[3]}")
                    print(f"Profesor: {curso[4]}")
                    print("Estudiantes:")
                    cursor.execute(
                        """
                        SELECT U.nombre_completo
                        FROM Matricula M
                        JOIN Usuario U ON M.id_usuario = U.documento_identidad
                        WHERE M.id_curso = %s
                        """,
                        (cid,)
                    )
                    for est in cursor.fetchall():
                        print(" -", est[0])
                else:
                    print("Curso no encontrado.")

            elif opt == "3":
                filtro = input("Filtrar por (rol/id/todos): ")
                if filtro == "rol":
                    rol = int(input("Tipo (0=Admin,1=Profesor,2=Estudiante): "))
                    cursor.execute("SELECT * FROM Usuario WHERE tipo = %s", (rol,))
                elif filtro == "id":
                    uid = int(input("ID del usuario: "))
                    cursor.execute(
                        "SELECT * FROM Usuario WHERE documento_identidad = %s",
                        (uid,)
                    )
                else:
                    cursor.execute("SELECT * FROM Usuario")
                for u in cursor.fetchall():
                    print(u)

            elif opt == "4":
                break
            else:
                print("Opción inválida.")
    finally:
        conn.close()

# ─── Parte 3: Menú y Funcionalidades Profesor/Alumno ──────────────────────────

def listar_mis_cursos(usuario):
    conn = conectar()
    cursor = conn.cursor()
    try:
        print("\n--- Mis Cursos ---")
        if usuario['tipo'] == 1:
            cursor.execute(
                "SELECT id_curso, nombre, semestre, ano "
                "FROM Curso WHERE profesor_asignado = %s",
                (usuario['documento_identidad'],)
            )
        else:
            cursor.execute(
                """
                SELECT C.id_curso, C.nombre, C.semestre, C.ano
                FROM Matricula M
                JOIN Curso C ON M.id_curso = C.id_curso
                WHERE M.id_usuario = %s
                """,
                (usuario['documento_identidad'],)
            )
        rows = cursor.fetchall()
        if rows:
            for r in rows:
                print(f"{r[0]} - {r[1]} (Sem {r[2]}-{r[3]})")
        else:
            print("No tienes cursos asignados.")
    finally:
        conn.close()

def listar_alumnos_curso(id_curso):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT U.documento_identidad, U.nombre_completo
            FROM Matricula M
            JOIN Usuario U ON M.id_usuario = U.documento_identidad
            WHERE M.id_curso = %s
            """,
            (id_curso,)
        )
        al = cursor.fetchall()
        print("\n--- Alumnos matriculados ---")
        if al:
            for a in al:
                print(f"{a[0]} - {a[1]}")
        else:
            print("No hay alumnos en este curso.")
    finally:
        conn.close()

def listar_materiales_curso(id_curso):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_material, titulo, descripcion, nombre_archivo "
            "FROM Material WHERE id_curso = %s",
            (id_curso,)
        )
        mats = cursor.fetchall()
        print("\n--- Materiales del curso ---")
        if mats:
            for mid, tit, desc, arc in mats:
                print(f"{mid} - {tit}: {desc} ({arc})")
        else:
            print("No hay materiales publicados.")
    finally:
        conn.close()

def listar_tareas_curso(id_curso):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_tarea, descripcion, fecha_entrega "
            "FROM Tarea WHERE id_curso = %s",
            (id_curso,)
        )
        tas = cursor.fetchall()
        print("\n--- Tareas asignadas ---")
        if tas:
            for t in tas:
                print(f"{t[0]} - {t[1]} (Entrega: {t[2]})")
        else:
            print("No hay tareas asignadas.")
    finally:
        conn.close()

def menu_foros(usuario, id_curso):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_foro, nombre FROM Foro WHERE id_curso = %s",
            (id_curso,)
        )
        foros = cursor.fetchall()
        if not foros:
            print("No hay foros en este curso.")
            return
        print("\n--- Foros disponibles ---")
        for f in foros:
            print(f"{f['id_foro']} - {f['nombre']}")
        id_foro = int(input("ID del foro a ingresar: "))
        if not any(f['id_foro'] == id_foro for f in foros):
            print("Foro no encontrado.")
            return

        while True:
            print("\n--- MENÚ FORO ---")
            print("1. Listar mensajes")
            print("2. Enviar mensaje")
            print("3. Responder mensaje")
            print("4. Salir del foro")
            op = input("Opción: ")
            if op == "1":
                cursor.execute(
                    """
                    SELECT M.id_mensaje, U.nombre_completo, M.descripcion, M.mensaje_referencia
                    FROM Mensaje M
                    JOIN Usuario U ON M.id_usuario = U.documento_identidad
                    WHERE M.id_foro = %s AND M.id_curso = %s
                    ORDER BY M.id_mensaje
                    """,
                    (id_foro, id_curso)
                )
                msgs = cursor.fetchall()
                print("\n--- Mensajes ---")
                for ms in msgs:
                    pref = f"(resp a {ms['mensaje_referencia']}) " if ms['mensaje_referencia'] else ""
                    print(f"{ms['id_mensaje']} - {ms['nombre_completo']} {pref}: {ms['descripcion']}")
            elif op == "2":
                titulo_m = input("Título del mensaje: ")
                texto    = input("Contenido: ")
                cursor.execute(
                    "INSERT INTO Mensaje "
                    "(nombre, descripcion, id_foro, id_usuario, id_curso, mensaje_referencia) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (titulo_m, texto, id_foro, usuario['documento_identidad'], id_curso, None)
                )
                conn.commit()
                print("Mensaje enviado.")
            elif op == "3":
                id_msg   = int(input("ID del mensaje a responder: "))
                titulo_r = input("Título de la respuesta: ")
                texto    = input("Contenido: ")
                cursor.execute(
                    "INSERT INTO Mensaje "
                    "(nombre, descripcion, id_foro, id_usuario, id_curso, mensaje_referencia) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (titulo_r, texto, id_foro, usuario['documento_identidad'], id_curso, id_msg)
                )
                conn.commit()
                print("Respuesta enviada.")
            elif op == "4":
                break
            else:
                print("Opción inválida.")
    finally:
        conn.close()

def subir_material(usuario, id_curso):
    if usuario['tipo'] != 1:
        print("Solo los profesores pueden subir materiales.")
        return
    conn = conectar()
    cursor = conn.cursor()
    try:
        tit  = input("Título del material: ")
        desc = input("Descripción: ")
        arc  = input("Nombre de archivo (ficticio): ")
        cursor.execute(
            "INSERT INTO Material (titulo, descripcion, nombre_archivo, id_curso) "
            "VALUES (%s, %s, %s, %s)",
            (tit, desc, arc, id_curso)
        )
        conn.commit()
        print("Material subido correctamente.")
    finally:
        conn.close()

def crear_foro(usuario, id_curso):
    if usuario['tipo'] != 1:
        print("Solo los profesores pueden crear foros.")
        return
    conn = conectar()
    cursor = conn.cursor()
    try:
        nom  = input("Nombre del foro: ")
        desc = input("Descripción: ")
        ft   = input("Fecha terminación (YYYY-MM-DD o vacío): ")
        fc   = date.today().isoformat()
        ft   = ft if ft.strip() else None
        cursor.execute(
            "INSERT INTO Foro "
            "(nombre, descripcion, fecha_creacion, fecha_terminacion, id_curso, id_profesor) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (nom, desc, fc, ft, id_curso, usuario['documento_identidad'])
        )
        conn.commit()
        print("Foro creado correctamente.")
    finally:
        conn.close()

def menu_curso(usuario, id_curso):
    # Verificar acceso
    conn = conectar()
    cur = conn.cursor()
    try:
        if usuario['tipo'] == 1:
            cur.execute(
                "SELECT 1 FROM Curso WHERE id_curso = %s AND profesor_asignado = %s",
                (id_curso, usuario['documento_identidad'])
            )
        else:
            cur.execute(
                "SELECT 1 FROM Matricula WHERE id_curso = %s AND id_usuario = %s",
                (id_curso, usuario['documento_identidad'])
            )
        if not cur.fetchone():
            print("No tienes acceso a ese curso.")
            return
    finally:
        conn.close()

    while True:
        print(f"\n--- MENÚ CURSO {id_curso} ---")
        print("1. Listar Alumnos")
        print("2. Listar Materiales")
        print("3. Foros")
        print("4. Tareas")
        if usuario['tipo'] == 1:
            print("5. Subir Materiales")
            print("6. Crear Foro")
            print("7. Salir del curso")
        else:
            print("5. Salir del curso")
        op = input("Opción: ")

        if op == "1":
            listar_alumnos_curso(id_curso)
        elif op == "2":
            listar_materiales_curso(id_curso)
        elif op == "3":
            menu_foros(usuario, id_curso)
        elif op == "4":
            listar_tareas_curso(id_curso)
        elif op == "5" and usuario['tipo'] == 1:
            subir_material(usuario, id_curso)
        elif op == "6" and usuario['tipo'] == 1:
            crear_foro(usuario, id_curso)
        elif (op == "7" and usuario['tipo'] == 1) or (op == "5" and usuario['tipo'] == 2):
            break
        else:
            print("Opción inválida.")

def menu_profesor_alumno(usuario):
    while True:
        print("\n--- MENÚ PROFESOR/ALUMNO ---")
        print("1. Listar mis cursos")
        print("2. Ingresar a un curso")
        print("3. Salir")
        op = input("Opción: ")
        if op == "1":
            listar_mis_cursos(usuario)
        elif op == "2":
            cid = int(input("ID del curso a ingresar: "))
            menu_curso(usuario, cid)
        elif op == "3":
            break
        else:
            print("Opción inválida.")

def menu_administrador():
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Crear nuevo usuario")
        print("2. Ver usuario")
        print("3. Matricular usuario a curso")
        print("4. Ver matrícula")
        print("5. Asignar profesor a curso")
        print("6. Reportes")
        print("7. Salir")
        op = input("Opción: ")
        if op == "1":
            crear_usuario()
        elif op == "2":
            ver_usuario()
        elif op == "3":
            matricular_usuario()
        elif op == "4":
            ver_matricula()
        elif op == "5":
            asignar_profesor()
        elif op == "6":
            menu_reportes()
        elif op == "7":
            break
        else:
            print("Opción inválida.")

def main():
    print("🎓 SISTEMA NODO - INICIO DE SESIÓN")
    usuario = None
    while not usuario:
        usuario = login()
    if usuario['tipo'] == 0:
        menu_administrador()
    else:
        menu_profesor_alumno(usuario)

if __name__ == "__main__":
    main()
