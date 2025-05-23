import argparse

from db_modulos.crea_db_hechos import creaDbUser, insercionDatosPrueba
from metodosAnalisis import ConsultasSql #Objeto de consultas

def main():
    # Recibimos el año
    parser = argparse.ArgumentParser(description="Analizar ventas de cine")
    parser.add_argument("anio", type=int, help="Año a analizar")
    anioAnalizis = parser.parse_args().anio

    # año recibido
    print(anioAnalizis)

    # Se crea la DB 'db_cine' con su respectivo esquema
    consultaExistenciaBD = str(input("Crear 'db_cine' con su respectivo esquema [Y/Yes = si, Cualquier Otro = no]: ")).lower()
    if(consultaExistenciaBD == "y" or consultaExistenciaBD == "yes"): creaDbUser()

    # Se insertan datos sobre la DB usando el User
    consultaInsercionBD = str(input("Ingresar datos de prueba a la base de datos [Y/Yes = si, Cualquier Otro = no]: ")).lower()
    if(consultaInsercionBD == "y" or consultaInsercionBD == "yes"): insercionDatosPrueba()
    
    # Se crea el objeto mediante el cual se realizarán las peticiones, para hacer distintos gráficos
    objectSql = ConsultasSql()

    try:
        while(True):
            peticion = str(input("""
    Que desea análizar sobre la base de datos?
    > El top 10 de las películas más vistas [1]
    > El top 10 de géneros menos vistos [2]
    > La ventas de algún año en particular [3]
    > Las ventas por género en algún año [4]
    > La edad por género de peliculas [5]
    > Películas con mayor recaudación mensual del año [6]
                """))
            
            match peticion:
                case "1":
                    objectSql.analisis_top_10_peliculas_mas_vistas(anioAnalizis)
                    break
                case "2":
                    objectSql.analisis_top_10_generos_menos_vistos(anioAnalizis)
                    break
                case "3":
                    objectSql.analisis_ventas_anuales(anioAnalizis)
                    break
                case "4":
                    objectSql.analisis_ventas_anuales_por_genero(anioAnalizis)
                    break
                case "5":
                    objectSql.analisis_edad_por_genero_pelicula(anioAnalizis)
                    break
                case "6":
                    objectSql.analisis_pelicula_con_mayor_recaudacion_por_mes(anioAnalizis)
                    break
                case _:
                    print("Ingrese algúna petición válida...\n")
    except Exception as e:
        print(f"Hubo un error al momento de realizar algún análisis\nDetalle -> {e}")
    finally:
        objectSql.cerrar()

if ("__main__" == __name__):
    main()