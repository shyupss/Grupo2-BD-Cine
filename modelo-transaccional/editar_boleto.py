import psycopg2
from datetime import datetime, timedelta
from conectar import conectar

def editarFuncion(cur, conn, idBoleto, idFuncion) -> None:

    # mostrar peliculas
    print("\nPelículas disponibles:")
    cur.execute('''
        SELECT id, titulo, genero, director, duracion
        FROM pelicula
        ORDER BY id
    ''')
    peliculas = cur.fetchall()
    for idPeli, nombrePeli, genero, directorPeli, duracionPeli in peliculas:
        print(f"[ID: {idPeli}] - {nombrePeli} | Género: {genero} | Director: {directorPeli} | Duración: {duracionPeli}")

    # seleccion pelicula
    eleccionPelicula = int(input("\nIndique el ID de la pelicula: "))
    cur.execute('''
        SELECT *
        FROM pelicula
        WHERE id = %s
    ''', (eleccionPelicula, ))
    row = cur.fetchone()
    if not row:
        print("No existe ninguna pelicula con ese ID.")
        conn.rollback()
        return

    # mostrar funciones
    fechaPrueba = datetime(2025, 4, 1, 0, 0)

    print("\nFunciones disponibles:")
    cur.execute(
        '''
        SELECT f.id, f.hora_inicio, f.hora_fin, f.id_sala
        FROM funcion f
        WHERE f.hora_fin > %s AND f.id_pelicula = %s AND id <> %s
        ''',
        (fechaPrueba, eleccionPelicula, idFuncion)
    )
    funciones = cur.fetchall()

    # DEBUG: ver NOW() y las funciones sin filtrar
    #cur.execute("SELECT NOW()")
    #print("AHORA:", cur.fetchone()[0])
    #cur.execute(
    #    '''
    #    SELECT id, hora_inicio, hora_fin
    #    FROM funcion
    #    WHERE id_pelicula = %s
    #    ORDER BY hora_inicio
    #    ''',
    #    (eleccionPelicula,)
    #)
    #print("TODAS LAS FUNCIONES (sin filtro):", cur.fetchall())
    
    if not funciones:
        print("No hay funciones disponibles para esta película en este momento.")
        return
    for func in funciones:
        idF, inicio, fin, sala = func
        print(f"[ID: {idF}] Inicia: {inicio} | Termina: {fin} | Sala: {sala}")
    
    # validando funcion a seleccionar
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
        if resultado[0] <= fechaPrueba:#datetime.now(): # si se halló, pero ya terminó
            print("Esta función ya terminó y no se pueden vender boletos.")
            continue
        funcion_validada = True

    # obtener datos de la sala de la funcion
    cur.execute(f"SELECT id_sala FROM funcion WHERE id = {id_funcion}")
    id_sala = cur.fetchone()[0] # id de sala obtenida
    cur.execute(f"SELECT cant_asientos FROM sala WHERE id = {id_sala}")
    cant_asientos = cur.fetchone()[0] # último número de asiento

    # --- Mostrar & Validar asiento ---

    # mostrar asientos
    cur.execute(
        '''
        SELECT a.num
        FROM asiento a
        LEFT JOIN boleto b ON b.id_funcion = %s AND a.num = b.num_asiento
        WHERE a.id_sala = %s AND b.id IS NULL
        ORDER BY a.num
        ''',
        (id_funcion, id_sala)
    )
    disponibles = [row[0] for row in cur.fetchall()]
    print(f"\nAsientos disponibles para la función {id_funcion} (Sala {id_sala}):\n{disponibles}\n")

    # validando asiento a seleccionar
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

    # actualizar el boleto con la nueva funcion y asiento
    try:
        cur.execute(
            '''
            UPDATE boleto
            SET id_funcion = %s,
                num_asiento = %s
            WHERE id = %s
            ''',
            (id_funcion, num_asiento, idBoleto)
        )
        conn.commit()
        print(f"Boleto {idBoleto} actualizado: función {id_funcion}, asiento {num_asiento}.")
    except Exception as e:
        conn.rollback()
        print(f"No se pudo actualizar el boleto: {e}")

def editarNumeroAsiento(existenciaBoleto: int) -> None:
    """
    Edita el número de asiento de un boleto existente.
    """
    conn = conectar()
    cur = conn.cursor()

    try:
        # Obtiene el número de asiento actual del boleto
        cur.execute(
            '''
            SELECT num_asiento
            FROM boleto
            WHERE id = %s
            ''',
            (existenciaBoleto[0][0],)
        )
        num_asiento_actual = cur.fetchone()[0]
        print(f"El número de asiento actual es: {num_asiento_actual}")

        nuevo_num_asiento = int(input("Ingrese el nuevo número de asiento: ").strip())

        # Verifica que el nuevo asiento no esté ocupado
        cur.execute(
            '''
            SELECT 1 FROM boleto
            WHERE num_asiento = %s AND id_funcion = %s
            ''',
            (nuevo_num_asiento, existenciaBoleto[0][1])
        )
        if cur.fetchone():
            print(f"El asiento {nuevo_num_asiento} ya está ocupado para la función {existenciaBoleto[0][1]}.")
            return

        # Actualiza el número de asiento
        cur.execute(
            '''
            UPDATE boleto
            SET num_asiento = %s
            WHERE id = %s
            ''',
            (nuevo_num_asiento, existenciaBoleto[0][0])
        )
        conn.commit()
        print(f"Número de asiento actualizado a {nuevo_num_asiento} para el boleto ID {existenciaBoleto[0][0]}.")

    except Exception as e:
        conn.rollback()
        print(f"No se pudo actualizar el número de asiento: {e}")
    finally:
        cur.close()
        conn.close()

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
        if not existenciaBoleto:
            print("No se puede editar un boleto que no está registrado...")
            return
        # De lo contrario, consultamos lo que se desea editar

        print("\n=== DATO DEL BOLETO A EDITAR ===\n")
        print("1. Función")
        print("2. Numero de asiento")
        print("s. Salir")

        opcion = input("Seleccione una opción: ")

        match opcion:
            case '1':
                editarFuncion(cur, conn, existenciaBoleto[0][0], existenciaBoleto[0][2])
            case '2':
                editarNumeroAsiento(existenciaBoleto)
            case 's':
                print("Saliendo de editar...")
            case _:
                ...

    except Exception as e:
        print(f"Error -> {e}")