import psycopg2

# Cerrar conexiones de forma segura
def cerrar_conexiones(**kwargs):
    for nombre, obj in kwargs.items():
        if obj:
            try: obj.close()
            except Exception as e: print(f"# Error al intentar cerrar '{nombre}'\nDetalle -> {e}")

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

    finally: cerrar_conexiones(conn_sr=conn_sr, cur_sr=cur_sr)