import gc
import psycopg2
import matplotlib

class SqlObj:

    # conexión a PostgreSQL hacia la bd con el user correspondiente
    def __init__(self, database, user, password, host):
        self.conn = None
        self.cur = None

        self.database = database
        self.user = user
        self.password = password
        self.host = host

        self.abrir_conexion()

    def __del__(self): self.cerrar_conexion(self)

    def abrir_conexion(self):
        try:
            self.conn = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host
            )
            self.cur = self.conn.cursor()
            print(f"> Conexión exitosa\nUser: {self.conn.info.user}\nBase de datos: {self.conn.info.dbname}")

        except Exception as e:
            SqlObj.cerrar_conexiones(conn=self.conn, cur=self.cur)
            print(f"# Error al conectarse hacia la base de datos.\nDetalle -> {e}")

    def cerrar_conexion(self): SqlObj.cerrar_conexiones(conn=self.conn, cur=self.cur)

    @staticmethod
    def cerrar_conexiones(**kwargs):
        for nombre, obj in kwargs.items():
            if obj:
                try: obj.close()
                except Exception as e: print(f"# Error al intentar cerrar '{nombre}'\nDetalle -> {e}")
                finally: obj = None
        gc.collect()