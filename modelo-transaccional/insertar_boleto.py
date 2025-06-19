import psycopg2
from datetime import datetime
from conectar import conectar

def insertar_boleto():
    conn = conectar()
    cur = conn.cursor()

    try:
        print("\n¿Tipo de compra?")
        print("1. Presencial")
        print("2. Online (nuevo cliente)")
        print("3. Online (cliente ya registrado)")
        tipo_compra = input("Seleccione (1, 2 o 3): ")

        id_cliente = None

        # Venta presencial
        if tipo_compra == "1":
            id_cliente = 1  # Cliente presencial estándar
                            # Está registrado en DB como "Venta Presencial"

        # Venta online para nuevo cliente
        elif tipo_compra == "2":
            nombres = input("Ingrese nombres del cliente: ").strip()
            apellidos = input("Ingrese apellidos del cliente: ").strip()
            edad = int(input("Ingrese edad del cliente: ").strip())
            cur.execute(f'''
                INSERT INTO cliente (nombres, apellidos, edad)
                VALUES ('{nombres}', '{apellidos}', {edad})
                RETURNING id
            ''')
            id_cliente = cur.fetchone()[0] # guarda ID nuevo cliente tras inserción en tabla cliente
            print(f"Cliente insertado con ID {id_cliente}")

        # Venta online para cliente ya registrado
        elif tipo_compra == "3":
            id_cliente = int(input("Ingrese el ID del cliente registrado: ").strip())
            cur.execute(f'SELECT 1 FROM cliente WHERE id = {id_cliente}')
            if not cur.fetchone(): # si no halló ID
                print("No existe este usuario.")
                return

        # Error al elegir opciones
        else:
            print("Opción inválida.")
            return

        # Una vez ya se manejó el ingreso de cliente

        # Enlistar funciones activas
        print("\nFunciones disponibles:")
        cur.execute('''
            SELECT f.id, p.titulo, f.hora_inicio, f.hora_fin, f.id_sala
            FROM funcion f
            JOIN pelicula p ON f.id_pelicula = p.id
            WHERE f.hora_fin > NOW()
            ORDER BY f.hora_inicio
        ''')
        funciones = cur.fetchall()
        for f in funciones:
            print(f"[{f[0]}] '{f[1]}' en sala {f[4]} / inicia: {f[2]} termina: {f[3]}")

        # Desde input se ingresa ID función
        funcion_validada = False
        while not funcion_validada:
            id_funcion = int(input("\nIngrese el ID de la función: ").strip())

            # Verificar que la función existe y está activa/disponible
            cur.execute(
                f"SELECT hora_fin FROM funcion WHERE id = {id_funcion}"
            )
            resultado = cur.fetchone()
            if not resultado: # si no se halló función en db
                print("Esta función no existe. Por favor, ingrese una función válida.")
                continue
            if resultado[0] <= datetime.now(): # si se halló, pero ya terminó
                print("Esta función ya terminó y no se pueden vender boletos.")
                continue
            funcion_validada = True

        cur.execute(f"SELECT id_sala FROM funcion WHERE id = {id_funcion}")
        id_sala = cur.fetchone()[0] # almacena id de sala obtenida

        # 5) Listar asientos libres
        cur.execute("""
            SELECT a.num
                FROM asiento a
            LEFT JOIN boleto b
                ON b.id_funcion = %s
                AND b.num_asiento = a.num
                WHERE a.id_sala = (
                    SELECT id_sala
                    FROM funcion
                    WHERE id = %s
                )
                AND b.id IS NULL
        """, (id_funcion, id_funcion))
        
        asientosLibres = cur.fetchall()
        for asiento in asientosLibres:
            print(f"Asiento [{asiento[0]}]", end=" _ ")

        print("\n")
        cur.execute(f"SELECT cant_asientos FROM sala WHERE id = {id_sala}")
        cant_asientos = cur.fetchone()[0] # almacena el último número de asiento

        asiento_validado = False
        while not asiento_validado:
            # Desde input se ingresa num. asiento
            num_asiento = int(input("Ingrese el número de asiento: ").strip())

            # Verificar que el asiento existe en la sala correspondiente
            cur.execute(
                f"SELECT 1 FROM asiento WHERE id_sala = {id_sala} AND num = {num_asiento}")
            if not cur.fetchone():
                print(f"El asiento {num_asiento} no existe en la sala {id_sala} de la función {id_funcion}.")
                print(f"La sala {id_sala} tiene asientos enumerados: desde 1 hasta {cant_asientos}.")
                print(f"Por favor, ingrese un asiento válido.")
                continue

            # Verificar que el asiento esté disponible para la venta del boleto
            cur.execute(
                f"SELECT 1 FROM boleto WHERE id_funcion = {id_funcion} AND num_asiento = {num_asiento}"
            )
            if cur.fetchone():
                print(f"El asiento {num_asiento} ya está ocupado para la función {id_funcion}.")
                print(f"Por favor, ingrese un asiento disponible.")
                continue

            asiento_validado = True

        # Desde input se ingresa el precio
        precio = int(input("Ingrese el precio del boleto: ").strip())

        # La hora de venta se obtiene directamente desde datetime.now()
        hora_compra = datetime.now()

        # Finalmente, se inserta boleto :)
        cur.execute(f'''
            INSERT INTO boleto (id_cliente, id_funcion, num_asiento, precio, hora_compra)
            VALUES ({id_cliente}, {id_funcion}, {num_asiento}, {precio}, '{hora_compra}')
            RETURNING id
        ''')
        id_boleto = cur.fetchone()
        conn.commit()
        print(f"Boleto vendido e insertado exitosamente con el ID: {id_boleto[0]}")

    except psycopg2.Error as error_postgres:
        conn.rollback()
        print(f"Error al insertar el boleto:\n{error_postgres.pgerror.strip()}")

    except ValueError as error_entrada:
        print(f"Error en la entrada de datos:\n{error_entrada}")

    finally:
        cur.close()
        conn.close()
