from insertar_funcion import insertar_funcion
from insertar_boleto import insertar_boleto
from editar_boleto import editar_boleto
from eliminar_boleto import eliminar_boleto

import sys

def menu():
    while True:
        print("\n=== MENÚ CINE ===")
        print("1. Insertar función")
        print("2. Insertar boleto")
        print("3. Editar boleto")
        print("4. Eliminar boleto")
        print("5. Listar boletos vendidos")
        print("5. Listar funciones")
        print("6. Editar función")
        print("7. Eliminar una próxima función")
        print("s. Salir")
        opcion = input("Seleccione una opción: ").strip().lower()

        match opcion:
            case '1':
                insertar_funcion()
            case '2':
                insertar_boleto()
            case '3':
                editar_boleto()
            case '4':
                eliminar_boleto()
            case 's':
                print("Saliendo del sistema.")
                break
            case _:
                print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario/terminal.")
        sys.exit(0)
