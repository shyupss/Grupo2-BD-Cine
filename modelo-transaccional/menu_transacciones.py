from insertar_funcion import insertar_funcion
from insertar_boleto import insertar_boleto
import sys

def menu():
    while True:
        print("\n=== MENÚ CINE ===")
        print("1. Insertar función")
        print("2. Insertar boleto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case '1':
                insertar_funcion()
            case '2':
                insertar_boleto()
            case '3':
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
