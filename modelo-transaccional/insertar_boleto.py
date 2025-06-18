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

        if tipo_compra == "1":
            id_cliente = 1  # Cliente presencial estándar
                            # Está registrado en DB como "Venta Presencial"

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

        elif tipo_compra == "3":
            id_cliente = int(input("Ingrese el ID del cliente registrado: ").strip())

        else:
            print("Opción inválida.")
            return

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

        id_funcion = int(input("\nIngrese el ID de la función: ").strip())
        num_asiento = int(input("Ingrese el número de asiento: ").strip())
        precio = int(input("Ingrese el precio del boleto: ").strip())
        hora_compra = datetime.now()

        # Insertar boleto
        cur.execute(f'''
            INSERT INTO boleto (id_cliente, id_funcion, num_asiento, precio, hora_compra)
            VALUES ({id_cliente}, {id_funcion}, {num_asiento}, {precio}, '{hora_compra}')
        ''')
        conn.commit()
        print("Boleto vendido e insertado exitosamente.")

    except psycopg2.Error as e:
        print(f"Error al insertar el boleto:\n{e.pgerror.strip()}")

    except ValueError as ve:
        print(f"Error en la entrada de datos:\n{ve}")

    finally:
        cur.close()
        conn.close()
