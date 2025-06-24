# Esta función inserta los datos de registros en tablas cliente, sala, pelicula
# de la cine_db_transaccional a la cine_db_relacional

def insertar_dimensiones(fuente_conn, dest_conn):
    with fuente_conn.cursor() as fuente_cur, dest_conn.cursor() as dest_cur: # alias para los cursores fuente y destino

        # Primero: insertar clientes
        print("-> -> Leyendo e insertando clientes...")
        fuente_cur.execute("SELECT id, nombres, apellidos, edad FROM cliente")
        dest_cur.executemany(
            "INSERT INTO cliente (id, nombres, apellidos, edad) VALUES (%s, %s, %s, %s)",
            fuente_cur.fetchall()
        )

        # Lo segundo: meter salas
        print("-> -> Leyendo e insertando salas...")
        fuente_cur.execute("SELECT id, tipo, cant_asientos FROM sala")
        dest_cur.executemany(
            "INSERT INTO sala (id, tipo, cant_asientos) VALUES (%s, %s, %s)",
            fuente_cur.fetchall()
        )

        # Y al final, meter las películas
        print("-> -> Leyendo e insertando películas...")
        fuente_cur.execute("SELECT id, titulo, director, duracion, sinopsis FROM pelicula")
        dest_cur.executemany(
            "INSERT INTO pelicula (id, titulo, director, duracion, sinopsis) VALUES (%s, %s, %s, %s, %s)",
            fuente_cur.fetchall()
        )

        # PENDIENTE
        #el %s sirve con tupla o lista? revisar si funciona bienel código
    dest_conn.commit()
