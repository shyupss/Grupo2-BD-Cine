import psycopg2
from conectar import conectar

def eliminar_boleto() -> None:
    """
    Permite eliminar un boleto existente después de confirmación.
    """
    conn = conectar()
    cur = conn.cursor()

    try:
        #id y verificar existencia
        id_boleto = int(input("Código identificador del boleto que desea eliminar: ").strip())
        cur.execute(
            "SELECT id, id_funcion, num_asiento FROM boleto WHERE id = %s",
            (id_boleto,)
        )
        boleto = cur.fetchone()
        if not boleto:
            print(f"No existe ningún boleto con ID {id_boleto}.")
            return

        # mostrar datos y pedir confirmación
        print(f"Boleto encontrado → ID: {boleto[0]}, Función: {boleto[1]}, Asiento: {boleto[2]}")
        confirm = input("¿Seguro que desea eliminar este boleto? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operación cancelada.")
            return

        # ejecutar DELETE y confirmar
        cur.execute(
            "DELETE FROM boleto WHERE id = %s",
            (id_boleto,)
        )
        conn.commit()
        print(f"Boleto {id_boleto} eliminado correctamente.")

    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar el boleto: {e}")

    finally:
        cur.close()
        conn.close()