import argparse

from db_modulos.crea_db_hechos import creaDbUser, insercionDatosPrueba
from metodosAnalisis import ConsultasSql #Objeto de consultas

DB_USER = "postgres"
DB_NAME = "cine_db_analisis"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

def main():
    # Recibimos el año
    parser = argparse.ArgumentParser(description="Analizar ventas de cine")
    parser.add_argument("anio", type=int, help="Año a analizar")
    anioAnalisis = parser.parse_args().anio

    # Se crea el objeto mediante el cual se realizarán las peticiones, para hacer distintos gráficos
    objectSql = ConsultasSql(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)

    try:
        while(True):
            print("\n--- ANÁLISIS AÑO " + str(anioAnalisis) + " ---")
            print("1. El top 10 de las películas que vendieron más boletos.")
            print("2. Los 10 géneros de películas que vendieron menos boletos.")
            print("3. Recaudación en ventas de cada mes del " + str(anioAnalisis) + ".")
            print("4. Las ventas de boletos por género de película.")
            print("5. Distribución de ventas por clasificación etaria (ATP, +13, +16, ...).")
            print("6. Las películas con mayor recaudación en cada mes del " + str(anioAnalisis) + ".")
            print("7. Generar todos los gráficos.")
            print("q. Salir.")
            peticion = str(input("Seleccione una opción: ")).strip().lower()
            
            match peticion:
                case "1":
                    objectSql.analisis_top_10_peliculas_mas_vistas(anioAnalisis)
                    break
                case "2":
                    objectSql.analisis_top_10_generos_menos_vistos(anioAnalisis)
                    break
                case "3":
                    objectSql.analisis_ventas_anuales(anioAnalisis)
                    break
                case "4":
                    objectSql.analisis_ventas_anuales_por_genero(anioAnalisis)
                    break
                case "5":
                    objectSql.analisis_ventas_clasificacion_etaria(anioAnalisis)
                    break
                case "6":
                    objectSql.analisis_pelicula_con_mayor_recaudacion_por_mes(anioAnalisis)
                    break
                case "7":
                    objectSql.analisis_top_10_peliculas_mas_vistas(anioAnalisis)
                    objectSql.analisis_top_10_generos_menos_vistos(anioAnalisis)
                    objectSql.analisis_ventas_anuales(anioAnalisis)
                    objectSql.analisis_ventas_anuales_por_genero(anioAnalisis)
                    objectSql.analisis_ventas_clasificacion_etaria(anioAnalisis)
                    objectSql.analisis_pelicula_con_mayor_recaudacion_por_mes(anioAnalisis)
                    break
                case "q":
                    print("Saliendo del sistema")
                    break
                case _:
                    print("Ingrese algúna petición válida...\n")
    except Exception as e:
        print(f"Hubo un error al momento de realizar algún análisis\nDetalle -> {e}")
    finally:
        objectSql.cerrar()

if ("__main__" == __name__):
    main()
