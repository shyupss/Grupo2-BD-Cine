import psycopg2

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

    def __del__(self):
        self.cerrar_conexion()

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
            print(f"# Error al conectarse hacia la base de datos.\nDetalle -> {e}")

    def cerrar_conexion(self): 
        if self.cur:
            try:
                self.cur.close()
            except Exception as e:
                print(f"Error al cerrar el cursor\nDetalle -> {e}")
            self.cur = None

        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                print(f"Error al cerrar la conexión\nDetalle -> {e}")
            self.conn = None