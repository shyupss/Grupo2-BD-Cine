import psycopg2

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
        except Exception as e:
            print(f"# Error al conectar a db_user\nDetalle -> {e}")

        # Insercion
        with open("./data/insercionDb.sql", 'r', encoding="utf-8") as f:
            script = f.read()
        
        for statement in script.split(';'):
            stmt = statement.strip()
            if stmt:
                cur_sr.execute(stmt + ';')
        
        conn_sr.commit()

        cur_sr.close()
        conn_sr.close()
        print("> Datos insertados con exito!")

        
    except Exception as e:
        print(f"Se ha producido un error al insertar los datos\nDetalle -> {e}")