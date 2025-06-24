def insertar_boletos(fuente_conn, dest_conn):
    with fuente_conn.cursor() as fuente_cur, dest_conn.cursor() as dest_cur: # alias fuente cursor y destino cursor
        print("-> -> -> Leyendo e insertando boletos en tabla de hechos...")
        fuente_cur.execute("""
        SELECT
            b.num_asiento, p.id, f.id_sala, c.id,
            f.hora_inicio, f.hora_fin,
            b.hora_compra, b.precio, p.genero, p.clasificacion_etaria
        FROM boleto b
        JOIN cliente c ON b.id_cliente = c.id
        JOIN funcion f ON b.id_funcion = f.id
        JOIN pelicula p ON f.id_pelicula = p.id
        """)
        dest_cur.executemany("""
        INSERT INTO hechos_boletos (
            num_asiento, id_pelicula, id_sala, id_cliente,
            hora_inicio_funcion, hora_fin_funcion,
            hora_compra, precio, genero, clasificacion_etaria
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, fuente_cur.fetchall())
    dest_conn.commit()
