from db_modulos.crea_db_hechos import creaDbUser, insercionDatosPrueba
from analisis import ConsultasSql #Objeto de consultas

def solicitaAnio():
    while True:
        anioSolicitado = str(input("Ingrese el año que desea analizar: "))
        if(anioSolicitado.isdigit):
            return int(anioSolicitado)
        else: print("Por favor, ingrese un año válido...")

def main():

    # Se crea la DB 'db_cine' con su respectivo esquema
    consultaExistenciaBD = str(input("Crear 'db_cine' con su respectivo esquema [Y/Yes = si, Cualquier Otro = no]: ")).lower()
    if(consultaExistenciaBD == "y" or consultaExistenciaBD == "yes"): creaDbUser()

    # Se insertan datos sobre la DB usando el User
    consultaInsercionBD = str(input("Ingresar datos de prueba a la base de datos [Y/Yes = si, Cualquier Otro = no]: ")).lower()
    if(consultaInsercionBD == "y" or consultaInsercionBD == "yes"): insercionDatosPrueba()
    
    # Se crea el objeto mediante el cual se realizarán las peticiones, para hacer distintos gráficos
    objectSql = ConsultasSql()

    while(True):
        peticion = str(input("""
Que desea análizar sobre la base de datos?
> El top 10 de las películas más vistas [1]
> El top 10 de géneros menos vistos [2]
> La ventas de algún año en particular [3]
> Las ventas por género en algún año [4]
> La edad por género de peliculas [5]
> Falta la última consulta [6]
              """))
        
        match peticion:
            case "1":
                objectSql.analisis_top_10_peliculas_mas_vistas(solicitaAnio())
                break
            case "2":
                objectSql.analisis_top_10_generos_menos_vistos(solicitaAnio())
                break
            case "3":
                objectSql.analisis_ventas_anuales(solicitaAnio())
                break
            case "4":
                objectSql.analisis_ventas_anuales_por_genero(solicitaAnio())
                break
            case "5":
                objectSql.analisis_edad_por_genero_pelicula(solicitaAnio())
                break
            case "6":
                # llamar al método restante
                break
            case default:
                print("Ingrese algúna petición válida...\n")

        seguir = str(input("Desea realizar otro análizis? [Y/Yes = si, Cualquier otro = no]")).lower()
        if(seguir != "y" or seguir != "yes"):
            break
    

if ("__main__" == __name__):
    main()