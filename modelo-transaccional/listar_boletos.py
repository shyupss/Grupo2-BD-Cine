import psycopg2
from datetime import datetime, timedelta
from conectar import conectar

def listar_boletos():
    conn = conectar()
    cur = conn.cursor()

    try:
        print("\nListar boletos vendidos en...")
        print("1. Últimos 7 días")
        print("2. Este mes")
        print("3. Este año")
        print("4. Todos")
        opcion = input("Seleccione una opción (1–4): ").strip()

        consulta_base = '''
            SELECT b.id, c.nombres, c.apellidos, p.titulo, s.id AS sala,
                   b.num_asiento, b.precio, b.hora_compra
            FROM boleto b
            JOIN cliente c ON b.id_cliente = c.id
            JOIN funcion f ON b.id_funcion = f.id
            JOIN pelicula p ON f.id_pelicula = p.id
            JOIN sala s ON f.id_sala = s.id
        ''' # consulta base que se hará según los requisitos del usuario

        if opcion == "1":
            desde = datetime.now() - timedelta(days=7) # a hoy le resto 7 días
            cur.execute(consulta_base + f" WHERE b.hora_compra >= '{desde}' ORDER BY b.hora_compra DESC")
            print("\nBoletos vendidos en los últimos 7 días:\n")

        elif opcion == "2":
            hoy = datetime.now()
            desde = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0) # cambia la fecha de búsqueda al primer día del mes
            cur.execute(consulta_base + f" WHERE b.hora_compra >= '{desde}' ORDER BY b.hora_compra DESC")
            print("\nBoletos vendidos en este mes:\n")

        elif opcion == "3":
            hoy = datetime.now()
            desde = hoy.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0) # fecha de búsqueda al 01 de enero
            cur.execute(consulta_base + f" WHERE b.hora_compra >= '{desde}' ORDER BY b.hora_compra DESC")
            print("\nBoletos vendidos en el último año:\n")

        elif opcion == "4":
            cur.execute(consulta_base + " ORDER BY b.hora_compra DESC")
            print("\nTodos los boletos vendidos:\n")

        else:
            print("Opción inválida.")
            return

        boletos = cur.fetchall()
        if not boletos:
            print("No se encontraron boletos.")
            return

        for b in boletos:
            print(f"[{b[0]}] Cliente: {b[1]} {b[2]} | Película: '{b[3]}' | Sala: {b[4]} | Asiento: {b[5]} | Precio: ${b[6]} | Hora: {b[7]}")

        print(f"Total de boletos listados: {len(boletos)}")


    except psycopg2.Error as error_postgres:
        conn.rollback()
        print(f"Error al listar boletos:\n{error_postgres.pgerror.strip()}")

    except ValueError as error_entrada:
        print(f"Error en la entrada de datos:\n{error_entrada}")

    finally:
        cur.close()
        conn.close()
