from conectar import conectar
from limpiar import limpiar
from insertar_dimensiones import insertar_dimensiones
from insertar_boletos import insertar_boletos
import schedule
import time
from datetime import datetime

import sys

def correr_etl():
    print("--- EJECUTANDO TAREA ETL ---")
    print(datetime.now().strftime("%H:%M:%S")) # para que se muestren los tiempos en consola
    try:
        fuente_conn = conectar("cine_db_transaccional") # conexión fuente (transaccional)
        dest_conn = conectar("cine_db_analisis") # conexión destino (análisis)
        limpiar(dest_conn)
        insertar_dimensiones(fuente_conn, dest_conn)
        insertar_boletos(fuente_conn, dest_conn)
        print("ETL completada.\n")
    except Exception as e:
        print("Error durante ETL:", e)
    finally:
        fuente_conn.close()
        dest_conn.close()

def ejecutar_etl_scheduled():
    schedule.every(5).minutes.do(correr_etl)
    print("Scheduler iniciado: ETL cada 5 minutos.")
    correr_etl()  # Ejecutar una vez al inicio
    while True: # Revisar tarea pendiente cada segundo
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        ejecutar_etl_scheduled()
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario/terminal.")
        sys.exit(0)
