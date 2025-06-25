from insertar_funcion import insertar_funcion
from insertar_boleto import insertar_boleto
from editar_boleto import editar_boleto
from eliminar_boleto import eliminar_boleto
from listar_boletos import listar_boletos
from listar_funciones import listar_funciones
from llenar_datos import llenar_datos

import sys

def menu():
    while True:
        print("\n=== MENÚ CINE ===")
        print("1. Insertar función")
        print("2. Insertar boleto")
        print("3. Editar boleto")
        print("4. Eliminar boleto")
        print("5. Listar boletos vendidos")
        print("6. Listar funciones")
        print("7. Llenar DB con nuevos datos")
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
            case '5':
                listar_boletos()
            case '6':
                listar_funciones()
            case '7':
                llenar_datos()
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
