import psycopg2
from datetime import datetime, timedelta
from conectar import conectar

def eliminar_boleto() -> None:

    # Declaro conexión
    conn = conectar()
    cur = conn.cursor()

    try:

        idBoleto = int(input("Código identificador del boleto que desea eliminar: ").strip())
        
        #Se recupera el boleto con la ID consultada
        cur.execute(f'''
            SELECT *
            FROM boleto
            WHERE id = '{idBoleto}'
        ''')

        # Se recupera la existencia
        existenciaBoleto = cur.fetchall()
        
        # Si no existe, se retorna (no se puede eliminar)
        if existenciaBoleto is None:
            print("No se puede editar un boleto que no está registrado...")
            return
        # De lo contrario, eliminamos secuencialmente en la base de datos
        

    except Exception:
        ...