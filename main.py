from db_modulos.crea_db_hechos import creaBdUser, insercionDatosPrueba

def main():

    # Se crea la DB 'db_cine' con su respectivo esquema
    consultaExistenciaBD = str(input("Crear 'db_cine' con su respectivo esquema [Y/Yes = si, Cualquier Otro = no]: ")).lower()
    if(consultaExistenciaBD == "y" or consultaExistenciaBD == "yes"): creaBdUser()

    # Se insertan datos sobre la DB usando el User
    consultaInsercionBD = str(input("Ingresar datos de prueba a la base de datos [Y/Yes = si, Cualquier Otro = no]: ")).lower()
    if(consultaInsercionBD == "y" or consultaInsercionBD == "yes"): insercionDatosPrueba()
    
    # Se crea el objeto mediante el cual se realizarán las peticiones, para hacer distintos gráficos
    # objectSql = SqlObj(None)

    while(True):
        print("wena")
        break

    

if ("__main__" == __name__):
    main()