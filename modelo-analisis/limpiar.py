def limpiar(conn, LOGGER):
    LOGGER.debug("Se ha ejecutado el método 'limpiar'.")

    with conn.cursor() as cur:
        print("-> Borrando datos de cine_db_analisis...")
        cur.execute("DELETE FROM hechos_boletos")
        cur.execute("DELETE FROM cliente")
        cur.execute("DELETE FROM sala")
        cur.execute("DELETE FROM pelicula")
    conn.commit()
