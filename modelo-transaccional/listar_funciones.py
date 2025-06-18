import psycopg2
from datetime import datetime
from conectar import conectar

def listar_funciones():
    conn = conectar()
    cur = conn.cursor()

    try:
        print("\n¿Qué funciones quiere que muestre el programa?")
        print("1. Funciones en curso (ahora mismo)")
        print("2. Próximas funciones")
        print("3. Funciones pasadas")
        opcion = input("Seleccione una opción (1–3): ").strip()

        consulta_base = '''
            SELECT f.id, p.titulo, s.id AS sala, f.hora_inicio, f.hora_fin
            FROM funcion f
            JOIN pelicula p ON f.id_pelicula = p.id
            JOIN sala s ON f.id_sala = s.id
        ''' # consulta base que se hará según lo que pida el usuario

        if opcion == "1":
            cur.execute(consulta_base + '''
                WHERE f.hora_inicio <= NOW() AND NOW() < f.hora_fin
                ORDER BY f.hora_inicio
            ''') # muestra las funciones que han iniciado pero que aún no han terminado
            print("\nFunciones en curso:\n")

        elif opcion == "2":
            cur.execute(consulta_base + '''
                WHERE f.hora_inicio > NOW()
                ORDER BY f.hora_inicio
            ''') # muestra las funciones que todavía no empiezan
            print("\nPróximas funciones:\n")

        elif opcion == "3":
            cur.execute(consulta_base + '''
                WHERE f.hora_fin < NOW()
                ORDER BY f.hora_inicio DESC
            ''') # muestra todas las funciones que ya terminaron
            print("\nFunciones pasadas:\n")

        else:
            print("Opción inválida.")
            return

        funciones = cur.fetchall()
        if not funciones:
            print("No se encontraron funciones.")
            return

        for f in funciones:
            print(f"[{f[0]}] '{f[1]}' | Sala {f[2]} | {f[3]} hasta {f[4]}")
        print(f"\nTotal de funciones listadas: {len(funciones)}")


    except psycopg2.Error as error_postgres:
        conn.rollback()
        print(f"Error al listar boletos:\n{error_postgres.pgerror.strip()}")

    except ValueError as error_entrada:
        print(f"Error en la entrada de datos:\n{error_entrada}")

    finally:
        cur.close()
        conn.close()

