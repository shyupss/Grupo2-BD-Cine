import psycopg2
import os

# RECORDAR
# Esta base de datos es distinta a la transaccional
# que armamos para la entrega pasada

# Script opcional!
# Solo correr si no se tiene cine_db_analisis
# o si no se tienen tablas definidas.
# Crea cine_db_analisis, las tablas definidas
# en crear_db_analisis.sql
# No se llenan! Eso se hace con la ETL

# Básicamente es casi el mismo código
# de la entrega pasada, pero crea otra
# base de datos: esta de análisis.
# Si quieren pueden modularizarlo aún más
# Y hacer que crear_db sirva para crear ambas
# bases de datos.

DB_NAME = "cine_db_analisis"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

def ejecutar_script(conn, path_sql):
    with open(path_sql, 'r', encoding='utf-8') as archivo:
        sql = archivo.read()

    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()
        print(f"Script ejecutado correctamente: {path_sql}")

def crear_base_de_datos():
    try:
        print(f"Conectando a la base postgres para crear '{DB_NAME}'...")
        conn = psycopg2.connect(
            dbname="postgres",  # conectar a la base de datos postgres (la que existe por defecto)
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Verifica si ya existe base de datos DB_NAME cine_db_analisis
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
        if cur.fetchone():
            print(f"La base de datos '{DB_NAME}' ya existe! No se crea nuevamente.")
        else:
            cur.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"Base de datos '{DB_NAME}' creada correctamente.")
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"No se pudo crear la base de datos:\n{e.pgerror.strip()}")
        return False
    return True

def inicializar_modelo_y_datos():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Conectado a la base de datos para ejecutar scripts...")

        ejecutar_script(conn, "scripts-sql/crear_db_analisis.sql") # Se declaran las tablas y sus campos

        conn.close()
        print("Base de datos inicializada correctamente.")

    except psycopg2.Error as e:
        print(f"No se pudo inicializar o llenar la base de datos:\n{e.pgerror.strip()}")

if __name__ == "__main__":
    if crear_base_de_datos(): # si se creó con éxito
        inicializar_modelo_y_datos() # se definen las tablas y se insertan los datos aleatorios (datos coherentes)
