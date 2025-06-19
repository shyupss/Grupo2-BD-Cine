import psycopg2
from datetime import datetime, timedelta
from conectar import conectar

def listar_boletos():
    conn = conectar()
    cur = conn.cursor()

    try:
        print("\nListar boletos vendidos...")
        print("1. En los últimos 7 días")
        print("2. En un mes y año específicos")
        print("3. Para una función específica")
        opcion = input("Seleccione una opción (1–3): ").strip()

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
            fecha_validada = False
            while not fecha_validada:
                try:
                    anio = int(input("Ingrese el año: ").strip())
                    mes = int(input("Ingrese el número del mes (1–12): ").strip())
                    if mes < 1 or mes > 12:
                        print("Mes inválido. Debe ser entre 1 y 12.")
                        continue

                    desde = datetime(anio, mes, 1) # desde el primer día del mes ingresado, del año ingresado
                    # Calcular el primer día del mes siguiente
                    if mes == 12:
                        hasta = datetime(anio + 1, 1, 1)
                    else:
                        hasta = datetime(anio, mes + 1, 1)
                    # hasta el primer día del mes siguiente

                    cur.execute(consulta_base + f'''
                        WHERE b.hora_compra >= '{desde}' AND b.hora_compra < '{hasta}'
                        ORDER BY b.hora_compra DESC
                    ''')
                    print(f"\nBoletos vendidos en {desde.strftime('%B %Y')}:\n") # convertir mes y año en string
                    fecha_validada = True

                except ValueError:
                    print("Entrada inválida. Debe ingresar números válidos para año y mes.")
                    continue

        elif opcion == "3":
            fecha_validada = False
            while not fecha_validada:
                try:
                    anio = int(input("Ingrese el año de la función: ").strip())
                    mes = int(input("Ingrese el mes de la función (1–12): ").strip())
                    if mes < 1 or mes > 12:
                        print("Mes inválido. Debe ser entre 1 y 12.")
                        continue

                    desde = datetime(anio, mes, 1)
                    if mes == 12:
                        hasta = datetime(anio + 1, 1, 1)
                    else:
                        hasta = datetime(anio, mes + 1, 1)

                    # Listar todas las funciones cuya hora_inicio esté en el rango
                    # de tiempo dispuesto por el usuario.
                    cur.execute(f'''
                        SELECT f.id, p.titulo, s.id AS sala, f.hora_inicio, f.hora_fin
                        FROM funcion f
                        JOIN pelicula p ON f.id_pelicula = p.id
                        JOIN sala s ON f.id_sala = s.id
                        WHERE f.hora_inicio >= '{desde}' AND f.hora_inicio < '{hasta}'
                        ORDER BY f.hora_inicio
                    ''')
                    funciones = cur.fetchall()

                    # Si no se halló función alguna en dicho rango de tiempo:
                    if not funciones:
                        print(f"No se encontraron funciones en {desde.strftime('%B %Y')}.")
                        continue

                    # En cambio, si se halló, entonces las enlisto :)
                    print(f"\nFunciones en {desde.strftime('%B %Y')}:")
                    for f in funciones:
                        print(f"[{f[0]}] '{f[1]}' | Sala {f[2]} | {f[3]} hasta {f[4]}")

                    fecha_validada = True

                except ValueError:
                    print("Entrada inválida. Debe ingresar números válidos para año y mes.")
                    continue

            # Ahora, consultar la función para la que quiere ver los boletos vendidos
            funcion_validada = False
            while not funcion_validada:
                try:
                    # Preguntarle al usuario de qué funcion quiere listar los boletos
                    id_funcion = int(input("\nIngrese el ID de la función para ver sus boletos vendidos: ").strip())

                    ids_funciones = [f[0] for f in funciones]
                    if id_funcion not in ids_funciones:
                        print("ID de función rechazado.")
                        print("Asegúrese de que sea el ID de una función en el mes y año ingresados.")
                        continue

                    cur.execute(consulta_base + f'''
                        WHERE b.id_funcion = {id_funcion}
                        ORDER BY b.hora_compra DESC
                    ''')

                    funcion_validada = True

                except ValueError:
                    print("Entrada inválida. Debe ingresar números válidos para ID.")
                    continue

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
