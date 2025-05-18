import psycopg2
import matplotlib
from relacionalBD.creaBdUser import creaBdUser
from relacionalBD.insercionBD import insercionDatosPrueba

class SqlPeticiones:

    def __init__(self, cur):
        # conexión a PostgreSQL hacia la bd con el user correspondiente
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="db_cine",
                user="user_cine",
                password="1234"
            )
            self.cur = conn.cursor()

        except Exception as e:
            self.cur = None
            print(f"Error al conectarse hacia la base de datos.\nDetalle --> {e}")

    def analisisVentasPorMes(año: int) -> None:
        ...

    def porcentajeProductosVendidos(año: int) -> None:
        ...

    def productoMasVendidoPorMes(año: int) -> None:
        ...

def main():

    # Se crea la DB 'db_cine' con su respectivo esquema
    consultaExistenciaBD = str(input("Si desea crear 'db_cine' con su respectivo esquema ingrese cualquier carácter, de lo contrario simplemente 'Enter': "))
    if(consultaExistenciaBD != ""):
        creaBdUser()

    # Se insertan datos sobre la DB usando el User
    consultaInsercionBD = str(input("Si desea ingresar datos de prueba a la DB, ingrese cualquier carácter, de lo contrario simplemente 'Enter': "))
    if(consultaInsercionBD != ""):
        insercionDatosPrueba() # Hay un error con la insercion de los datos, falta solucionar

    # Se crea el objeto mediante el cual se realizarán las peticiones, para hacer distintos gráficos
    objectSql = SqlPeticiones(None)

    while(True):
        print("wena")
        break

    

if ("__main__" == __name__):
    main()