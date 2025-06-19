import psycopg2
from datetime import datetime, timedelta
from conectar import conectar

def editarFuncion(idBoleto: str, idCliente: int, idFuncion: int, numAsiento: int, precio: int, cur, conn) -> None:

    # Mostrar películas disponibles
    print("\nPelículas disponibles:")
    cur.execute('''
        SELECT id, titulo, genero, director, duracion
        FROM pelicula
        ORDER BY id
    ''')
    peliculas = cur.fetchall()

    # Enlistando en ciclo for each
    for idPeli, nombrePeli, genero, directorPeli, duracionPeli in peliculas:
        print(f"[ID: {idPeli}] - {nombrePeli} | Género: {genero} | Director: {directorPeli} | Duración: {duracionPeli}")

    # Elegir pelicula
    eleccionPelicula = int(input("\nIndique el ID de la pelicula: "))

    # Elegir la funcion para esta pelicula
    # Listamos las funciones disponibles para esta pelicula (ignorando la antigua)
    cur.execute('''
        SELECT id, hora_inicio, hora_fin
        FROM funcion
        WHERE id_pelicula = %s
        AND id <> %s
    ''', (eleccionPelicula, idFuncion))

    funcionesDisponibles = cur.fetchall()

    # Mostramos las funciones
    for id_funcc, hora_ini, hora_fin in funcionesDisponibles:
        print(f"[ID: {id_funcc}] - Hora Inicio: {hora_ini} - Hora Fin: {hora_fin}")

    eleccionFuncion = int(input("Indique la funcion nueva que desea reservar: "))

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
    """, (eleccionFuncion, eleccionFuncion))
    
    asientosLibres = cur.fetchall()
    for asiento in asientosLibres:
        print(f"Asiento [{asiento[0]}]", end=" _ ")

    print("\n")
    numAsientoNuevo = input("Seleccione el asiento: ")

    # Se actualiza la funcion...
    cur.execute("""
            UPDATE boleto
               SET id_funcion  = %s,
                   num_asiento = %s
             WHERE id = %s
        """, (eleccionFuncion, numAsientoNuevo, idBoleto))
    
    conn.commit()
    print("Boleto actualizado exitosamente...")

def editarNumeroAsiento(existenciaBoleto: int) -> None:
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
                editarFuncion(existenciaBoleto[0][0], existenciaBoleto[0][1], 
                              existenciaBoleto[0][2], existenciaBoleto[0][3], 
                              existenciaBoleto[0][4], cur, conn)
            case '2':
                editarNumeroAsiento(existenciaBoleto)
            case 's':
                print("Saliendo de editar...")
            case _:
                ...

    except Exception as e:
        print(f"Error -> {e}")