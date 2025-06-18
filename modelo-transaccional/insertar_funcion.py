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

        # Ingreso de datos (película a proyectar,
        # sala donde se va a proyectar,
        # hora de inicio de la función)
        id_pelicula = int(input("\nIngrese el ID de la película: ").strip())
        id_sala = int(input("Ingrese el ID de la sala: ").strip())
        hora_inicio_str = input("Ingrese la hora de inicio (formato: YYYY-MM-DD HH:MM): ")

        # Parsear hora_inicio
        hora_inicio = datetime.strptime(hora_inicio_str, "%Y-%m-%d %H:%M")

        # Obtener duración de la película seleccionada
        cur.execute(f"SELECT duracion FROM pelicula WHERE id = {id_pelicula}")
        duracion = cur.fetchone()
        if not duracion:
            print("Error: la película no existe.") # si la película que ingresó no existe
            return # retorna y termina

        # Si existe, se calcula hora_fin en base a la duración
        duracion_tiempo = duracion[0]
        hora_fin = hora_inicio + timedelta(
            hours=duracion_tiempo.hour,
            minutes=duracion_tiempo.minute,
            seconds=duracion_tiempo.second
        )

        # Y por último se inserta la función para la película
        cur.execute(f'''
            INSERT INTO funcion (id_sala, id_pelicula, hora_inicio, hora_fin)
            VALUES ({id_sala}, {id_pelicula}, '{hora_inicio}', '{hora_fin}')
        ''')
        conn.commit()
        print(f"\nFunción insertada con éxito. Hora de fin calculada: {hora_fin}")

    except psycopg2.Error as e:
        print(f"Error al insertar función:\n{e.pgerror.strip()}")

    except ValueError as ve:
        print(f"Error en el formato de fecha/hora:\n{ve}")

    finally:
        cur.close()
        conn.close()
