import psycopg2
from getpass import getpass

# Crea la base de datos, el usuario, su contraseña y otorga los permisos al usuario desde el user "postgress"
def crear_db_cine(conn, cur, clave):

    try:
        conn.set_session(autocommit=True)

        # Crear la base de datos
        cur.execute("CREATE DATABASE db_cine;")

        # Crear el usuario para la base de datos
        cur.execute("CREATE USER user_cine WITH PASSWORD '1234';")
        cur.execute("GRANT CONNECT ON DATABASE db_cine TO user_cine;")

        print("> Base de datos 'db_cine' creada")
        print("> Usuario creado exitosamente\nNombre: user_cine\nContraseña: 1234")

        conn.set_session(autocommit=False)

        # Conectarse a la nueva base de datos
        conn_sr = psycopg2.connect(
            database="db_cine",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()

        # Otorgar permisos a usuario_emprendimiento
        cur_sr.execute("GRANT USAGE, CREATE ON SCHEMA public TO user_cine;")
        cur_sr.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO user_cine;")
        cur_sr.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO user_cine;")
        conn_sr.commit()
        print("> Permisos para user_cine concedidos con éxito")

        # Cerrar conexión de postgres a db_user
        cur_sr.close()
        conn_sr.close()

    except Exception as e:
        conn.rollback()
        print(f"# Error con la creación de db_cine\nDetalle -> {e}")

# Crea el modelo de la bd
def crear_esquema_db():

    run_script = True

    # Conexión a la nueva base de datos
    try:
        conn_sr = psycopg2.connect(
            database="db_cine",
            user="user_cine",
            password="1234",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()
        print("> postgres conectado con éxito a db_cine")
    except Exception as e:
        run_script = False
        print(f"# Error al conectar a db_user\nDetalle -> {e}")
    
    # Crear el modelo
    if run_script:
        try:
            with open("./data/modeloDb.sql", 'r', encoding="utf-8") as f:
                script = f.read()
            
            for statement in script.split(';'):
                stmt = statement.strip()
                if stmt:
                    cur_sr.execute(stmt + ';')

            conn_sr.commit()
            print("> Modelo de base de datos creado con éxito")

        except Exception as e:
            conn_sr.rollback()
            print(f"# Error con la creación del esquema\nDetalle -> {e}")
        
        cur_sr.close()
        conn_sr.close()

def creaBdUser(): #funcion exportada hacia main.py
    
    # Conexión a postgres en ámbito global
    clave = getpass("Ingrese su contraseña del usuario postgres: ")
    try: 
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=f"{clave}",
            host="localhost"
        )
        cur = conn.cursor()
        print(f"> Conexión exitosa\nUser: {conn.info.user}\nBase de datos: {conn.info.dbname}")
        
        crear_db_cine(conn, cur, clave)
        crear_esquema_db()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"# Fallo de conexión\nDetalle: {e}")