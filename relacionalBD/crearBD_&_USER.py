import psycopg2
from getpass import getpass

# Crea la base de datos, el usuario, su contraseña y otorga los permisos al usuario desde el user "postgress"
def crear_inventario_emprendimiento():
    '''
    Crea la base de datos 'bd_cine' y luego a su usuario 'user_cine' 
    junto con sus permisos.
    '''
    try:
        conn.set_session(autocommit=True)

        # Crear la base de datos
        cur.execute("CREATE DATABASE bd_cine;")

        # Crear el usuario para la base de datos
        cur.execute("CREATE USER user_cine WITH PASSWORD '1234';")
        cur.execute("GRANT CONNECT ON DATABASE bd_cine TO user_cine;")

        print("> Base de datos inventario_emprendimiento creada")
        print("> Usuario creado exitosamente\nNombre: user_cine\nContraseña: 1234")

        conn.set_session(autocommit=False)

        # Conectarse a la nueva base de datos
        conn_sr = psycopg2.connect(
            database="bd_cine",
            user="user_cine",
            password=f"{clave}",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()

        # Otorgar permisos a usuario_emprendimiento
        cur_sr.execute("GRANT USAGE ON SCHEMA public TO user_cine;")
        cur_sr.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO user_cine;")
        cur_sr.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO user_cine;")
        conn_sr.commit()
        print("> Permisos para usuario_emprendimiento concedidos con éxito")

        # Cerrar conexión de postgres a inventario_emprendimiento
        cur_sr.close()
        conn_sr.close()

    except Exception as e:
        conn.rollback()
        print(f"# Error con la creación de inventario_emprendimientos\nDetalle -> {e}")

# Crea el modelo de la bd
def crear_esquema_bd():
    '''
    Crea el esquema de la base de datos de análisis del sistema de emprendimiento\n
    Tener el archivo sql en la misma carpeta que este script python pls\n
    Link dbdiagram: https://dbdiagram.io/d/InventarioEmprendimiento-681f06245b2fc4582fff5e2b
    '''
    run_script = True

    # Conexión a la nueva base de datos
    try:
        conn_sr = psycopg2.connect(
            database="bd_cine",
            user="user_cine",
            password=f"{clave}",
            host="localhost"
        )
        cur_sr = conn_sr.cursor()
        print("> postgres conectado con éxito a inventario_emprendimiento")
    except Exception as e:
        run_script = False
        print(f"# Error al conectar a inventario_emprendimiento\nDetalle -> {e}")
    
    # Crear el modelo
    if run_script:
        try:
            with open("./data/modeloCine.sql", 'r', encoding="utf-8") as f:
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

if __name__ == "__main__":
    
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
        crear_inventario_emprendimiento()
        crear_esquema_bd()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"# Fallo de conexión\nDetalle: {e}")