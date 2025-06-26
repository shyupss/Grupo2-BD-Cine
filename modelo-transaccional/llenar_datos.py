import psycopg2
from conectar import conectar

def llenar_datos():
    print("\nEste proceso vaciará la base de datos cine_db_transacciones")
    print("y la volverá a llenar con datos aleatorios generados desde el script:")
    print("script-sql/insertar_datos_transaccional.sql")
    confirmacion = input("\n¿Está seguro de que desea vaciar y volver a llenar la base de datos? (s/n): ").strip().lower()
    if confirmacion != 's':
        print("Operación cancelada por el usuario.")
        return

    conn = conectar()
    cur = conn.cursor()

    try:
        print("\nVaciando base de datos...")

        # En orden de dependencia (el más dependiente de FK hasta el menos)
        tablas = ['boleto', 'funcion', 'asiento', 'sala', 'pelicula', 'cliente']
        for tabla in tablas:
            cur.execute(f"DELETE FROM {tabla};")

        conn.commit()
        print("Tablas vaciadas exitosamente.")

        # Reiniciar seriales (id) desde 1
        secuencias = [
            'cliente_id_seq',
            'pelicula_id_seq',
            'sala_id_seq',
            'funcion_id_seq',
            'boleto_id_seq'
        ]
        for seq in secuencias:
            cur.execute(f"ALTER SEQUENCE {seq} RESTART WITH 1;")

        # Ejecutar script para insertar datos
        print("Cargando nuevoss datos...")
        with open("scripts-sql/insertar_datos_transaccional.sql", "r", encoding="utf-8") as archivo:
            sql = archivo.read()
            cur.execute(sql)
        conn.commit()

        print("Datos insertados correctamente.")

    except psycopg2.Error as e:
        print("Error durante la operación:")
        print(e.pgerror.strip())
        conn.rollback()

    finally:
        cur.close()
        conn.close()
