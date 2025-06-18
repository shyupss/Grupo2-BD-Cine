import psycopg2
from datetime import datetime, timedelta
from conectar import conectar

def editarFuncion(idBoleto: int) -> None:
    ...

def editarNumeroAsiento(idBoleto: int) -> None:
    ...

def editarPrecio(idBoleto: int) -> None:
    ...

def editar_boleto():

    # Declaro conexión
    conn = conectar()
    cur = conn.cursor()

    try:
        idBoleto = int(input("Código identificador del boleto que desea editar: ").strip())
        
        #Se recupera el boleto con la ID consultada
        cur.execute(f'''
            SELECT *
            FROM boleto
            WHERE id = '{idBoleto}'
        ''')

        # Se recupera la existencia
        existenciaBoleto = cur.fetchall()
        
        # Si no existe, se retorna
        if existenciaBoleto is None:
            print("No se puede editar un boleto que no está registrado...")
            return
        # De lo contrario, consultamos lo que se desea editar

        print("\n=== DATO DEL BOLETO A EDITAR ===")
        print("1. Función")
        print("2. Numero de asiento")
        print("3. Precio")

        opcion = input("Seleccione una opción: ").strip()

        match opcion:
            case '1':
                ...
            case '2':
                ...
            case '3':
                ...

    except Exception:
        ...