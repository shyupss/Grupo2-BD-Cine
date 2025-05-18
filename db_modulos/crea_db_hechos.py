import psycopg2

from db_modulos.obj_sql import SqlObj
from getpass import getpass

# Crea la base de datos, el usuario, su contraseña y otorga los permisos al usuario desde el user "postgress"
def crear_db_cine(conn, cur, clave):

    # Verificar si la base de datos ya existe
    def existe_database():
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'db_cine';")
        if cur.fetchone() is None: return False
        else: return True

    # Verificar si el usuario ya existe
    def existe_usuario():
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname = 'user_cine';")
        if cur.fetchone() is None: return False
        else: return True

    # Crear la base de datos
    def crear_database():
        if not existe_database():
            cur.execute("CREATE DATABASE db_cine;")
            print("> Base de datos 'db_cine' creada")

        else: print("> La base de datos 'db_cine' ya existe, omitiendo creación")

    # Crear el usuario para la base de datos
    def crear_usuario():
        if not existe_usuario():
            cur.execute("CREATE USER user_cine WITH PASSWORD '1234';")
            cur.execute("GRANT CONNECT ON DATABASE db_cine TO user_cine;")
            print("> Usuario creado exitosamente\nNombre: user_cine\nContraseña: 1234")

        else: print("> El usuario 'user_cine' ya existe, omitiendo creación")

    # Otorgar permisos a usuario_emprendimiento
    def dar_permisos():
        cur_sr.execute("GRANT USAGE, CREATE ON SCHEMA public TO user_cine;")
        cur_sr.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO user_cine;")
        cur_sr.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO user_cine;")
        conn_sr.commit()
        print("> Permisos para user_cine concedidos con éxito")

    # Logica principal de la función: Bloque try-except-finally
    cur_sr = None
    conn_sr = None
    try:
        conn.set_session(autocommit=True)
        crear_database()
        crear_usuario()
        conn.set_session(autocommit=False)

        # Conectarse a la nueva base de datos
        conn_sr = psycopg2.connect(
            database="db_cine",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()

        dar_permisos()

    except Exception as e:
        conn.rollback()
        print(f"# Error con la creación de db_cine\nDetalle -> {e}")





# Crea el modelo de la bd
def crear_esquema_db(conn, cur):
        try:
            with open("./data/modeloDb.sql", 'r', encoding="utf-8") as script:
                cur.execute(script.read())
                conn.commit()

            print("> Modelo de base de datos creado con éxito")

        except Exception as e:
            conn.rollback()
            print(f"# Error con la creación del esquema\nDetalle -> {e}")





def creaBdUser(): #funcion exportada hacia main.py
    
    # Conexión a postgres en ámbito global
    clave = getpass("Ingrese su contraseña del usuario postgres: ")
    try:
        # Conexión a postgres como superusuario para crear db, esquemas y usuario
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur = conn.cursor()
        print(f"> Conexión exitosa\nUser: {conn.info.user}\nBase de datos: {conn.info.dbname}")

        crear_db_cine(conn, cur, clave)
        SqlObj.cerrar_conexiones(conn=conn, cur=cur)

        # Conexión a postgres como usuario especifico del codigo
        conn = psycopg2.connect(
            database="db_cine",
            user="user_cine",
            password="1234",
            host="localhost"
        )
        cur = conn.cursor()
        print(f"> Conexión exitosa\nUser: {conn.info.user}\nBase de datos: {conn.info.dbname}")
        
        crear_esquema_db(conn, cur)
        SqlObj.cerrar_conexiones(conn=conn, cur=cur)

    except Exception as e:
        conn.rollback()
        print(f"# Fallo de conexión\nDetalle -> {e}")

    finally: SqlObj.cerrar_conexiones(conn=conn, cur=cur)





# Inserta datos a través de la ejecución de un script .sql
def insercionDatosPrueba():

    try:
        # Conexion
        try:
            conn_sr = psycopg2.connect(
                database="db_cine",
                user="user_cine",
                password="1234",
                host="localhost"
            )
            cur_sr = conn_sr.cursor()
            print("> postgres conectado con éxito a db_cine")

        except Exception as e: print(f"# Error al conectar a db_user\nDetalle -> {e}")

        # Insercion
        with open("./data/insercionDb.sql", 'r', encoding="utf-8") as script:
            cur_sr.execute(script.read())
            conn_sr.commit()

        print("> Datos insertados con exito!")
        
    except Exception as e: print(f"Se ha producido un error al insertar los datos\nDetalle -> {e}")

    finally: SqlObj.cerrar_conexiones(conn_sr=conn_sr, cur_sr=cur_sr)