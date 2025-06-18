import psycopg2
from datetime import datetime, timedelta
from conectar import conectar

def insertar_funcion():
    conn = conectar()
    cur = conn.cursor()

    try:
        # Mostrar películas disponibles
        print("\nPelículas disponibles:")
        cur.execute('''
            SELECT id, titulo, genero, director, duracion
            FROM pelicula
            ORDER BY id
        ''')
        peliculas = cur.fetchall()

        # Enlistando en ciclo for each
        for peli in peliculas:
            print(f"[{peli[0]}] {peli[1]} | Género: {peli[2]} | Director: {peli[3]} | Duración: {peli[4]}")

        # Desde input, ingresar el ID de película y validar
        pelicula_validada = False
        while not pelicula_validada:
            id_pelicula = int(input("\nIngrese el ID de la película: ").strip())

            # Obtener duración de la película seleccionada
            cur.execute(f"SELECT duracion FROM pelicula WHERE id = {id_pelicula}")
            duracion = cur.fetchone()
            if not duracion:
                print("Error: la película no existe. Ingrese una película válida.") # si la película que ingresó no existe
                continue

            pelicula_validada = True

        # Desde input, ingresar hora de inicio de la función y validar
        horario_validado = False
        while not horario_validado:
            hora_inicio_str = input("Ingrese la hora de inicio (formato: YYYY-MM-DD HH:MM): ")
            # Parsear hora_inicio y calcular hora de término
            hora_inicio = datetime.strptime(hora_inicio_str, "%Y-%m-%d %H:%M")
            duracion_tiempo = duracion[0]
            hora_fin = hora_inicio + timedelta(
                hours=duracion_tiempo.hour,
                minutes=duracion_tiempo.minute,
                seconds=duracion_tiempo.second
            )
            print(f"Hora de fin calculada: {hora_fin}.")

            # Verificar salas disponibles que no tengan funciones en ese horario
            cur.execute(f'''
                SELECT id, tipo FROM sala
                WHERE id NOT IN (
                    SELECT id_sala FROM funcion
                    WHERE NOT (
                        '{hora_fin}' <= hora_inicio OR
                        '{hora_inicio}' >= hora_fin
                    )
                )
                ORDER BY id
            ''')
            salas_disponibles = cur.fetchall()

            if not salas_disponibles:
                print("No hay salas disponibles para este horario. Intente con otra hora.")
                continue  # vuelve a pedir otra hora

            print("Salas disponibles para este horario:")
            for sala in salas_disponibles:
                print(f"- Sala {sala[0]} | {sala[1]}") # muestra el número de la sala y el tipo (normal, imax, 3d, vip, etc)

            horario_validado = True

        # Pedir ID de sala y verificar que esté disponible
        salas_ids_disponibles = {s[0] for s in salas_disponibles} # enlistar salas disponibles por id
        sala_validada = False
        while not sala_validada:
            id_sala = int(input("Ingrese el ID de la sala que desea usar: ").strip())
            if id_sala in salas_ids_disponibles:
                sala_validada = True
            else:
                print("Sala no disponible en ese horario. Seleccione una de las salas listadas.")
                continue

        # Y por último se inserta la función para la película
        cur.execute(f'''
            INSERT INTO funcion (id_sala, id_pelicula, hora_inicio, hora_fin)
            VALUES ({id_sala}, {id_pelicula}, '{hora_inicio}', '{hora_fin}')
        ''')
        conn.commit()
        print(f"\nFunción insertada con éxito en sala {id_sala}. Horario: {hora_inicio} -- {hora_fin}")

    except psycopg2.Error as error_postgres:
        conn.rollback()
        print(f"Error al insertar la función:\n{error_postgres.pgerror.strip()}")

    except ValueError as error_entrada:
        print(f"Error en la entrada de datos:\n{error_entrada}")

    finally:
        cur.close()
        conn.close()
