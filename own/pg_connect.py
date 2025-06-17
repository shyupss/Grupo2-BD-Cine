from . import psycopg2, messagebox, cursor, connection

class PgConnect:
    def __init__(self, *args, **kwargs):
        '''Clase que maneja la conexión con postgres.'''
        self.__verbose:tuple[bool,bool] = (True, False)
        self.__params:dict[str:str] = {}

        self.__conexion:connection = None
        self.__cursor:cursor = None

        self.__databases:list[str] = []
        self.__database:str = ""

        self.__tablas:list[str] = []
        self.__tabla:str = ""

    @property
    def verbose(self):
        '''Identifica si el feedback de ejecución se dá a través de consola o interfaz gráfica con tkinter.'''
        return self.__verbose
    
    @verbose.setter
    def verbose(self, verb:tuple[bool,bool]):
        if len(verb) != 2: raise ValueError("La tupla debe identificar (consola, gui) donde consola:bool y gui:bool")
        if not isinstance(verb[0],bool) or not isinstance(verb[1], bool): raise ValueError("La tupla debe identificar (consola, gui) donde consola:bool y gui:bool")
        
        self.__verbose = verb

    @property
    def params(self):
        return self.__params

    @property
    def conexion(self):
        '''Objeto conexion de la librería 'psycopg2'.'''
        return self.__conexion
    
    @conexion.setter
    def conexion(self, con:dict[str,str]):
        self.conectarse(**con)
    
    @property
    def cursor(self):
        '''Objeto cursor de la librería 'psycopg2'.'''
        return self.__cursor
    
    @property
    def databases(self):
        '''Lista de Bases de Datos disponibles en la conexión.'''
        return self.__databases
    
    @property
    def database(self):
        '''Base de datos actualmente conectada.'''
        return self.__database
    
    @database.setter
    def database(self, db:str|int):
        self.cambiar_database(db)

    @property
    def tablas(self):
        '''Lista de tablas disponibles en la base de datos actual.'''
        return self.__tablas
    
    @property
    def tabla(self):
        return self.__tabla
    
    @tabla.setter
    def tabla(self, tbl:str):
        self.cambiar_tabla(tbl)
    
    def conectarse(self, **kwargs):
        try:
            conn = psycopg2.connect(**kwargs)

            self.desconectarse()

            if self.__verbose[0]: print("Se estableció la conexión con la base de datos correctamente.")
            if self.__verbose[1]: messagebox.showinfo("Conexión exitosa", "Se estableció la conexión con la base de datos correctamente.")

            return True

        except Exception as e:
            conn = None

            if self.__verbose[0]: print(f"No se pudo conectar a la base de datos:\n{e}")
            if self.__verbose[1]: messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{e}")

            return False

        finally:
            self.__conexion = conn
            if self.__conexion:
                self.__params = kwargs
                self.refrescar_databases()
                self.refrescar_tablas()
            else:
                self.__params = {}
    
    def desconectarse(self):
        if self.__cursor is not None:
            try: self.__cursor.close()

            except Exception as e:
                if self.__verbose[0]: print(f"Error al cerrar cursor:\n{e}")
                if self.__verbose[1]: messagebox.showinfo("Cursor Error", f"Error al cerrar cursor:\n{e}")

        if self.__conexion is not None:
            try: self.__conexion.close()

            except Exception as e:
                if self.__verbose[0]: print(f"Error al desconectar:\n{e}")
                if self.__verbose[1]: messagebox.showinfo("Desconexión", f"Error al desconectar:\n{e}")

        self.__params     = {}
        self.__cursor     = None
        self.__conexion   = None
        self.__verbose    = (True, False)
        self.__databases  = []
        self.__database   = ""
        self.__tablas     = []
        self.__tabla      = ""

        if self.__verbose[0]: print("Desconectado y estado interno restablecido.")
        if self.__verbose[1]: messagebox.showinfo("Desconexión", "Se ha cerrado la conexión y se restableció el estado.")
    
    def refrescar_cursor(self):
        '''Recarga el cursor de la conexión para un nuevo uso o inicializarlo.'''

        ### Validaciones:
        if not self.__conexion: raise ConnectionError("No hay conexión para extraer cursor.")

        ### Código:
        self.__cursor = self.__conexion.cursor()

    def refrescar_databases(self):
        '''Si existe una conexión, retorna las bases de datos disponibles y selecciona una base de datos.'''

        ### Validaciones:
        if not self.__conexion: raise ConnectionError("No hay conexión para extraer databases.")

        ### Código:
        self.refrescar_cursor()
        self.__cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases:list[str] = [db[0] for db in self.__cursor.fetchall()]
        self.refrescar_cursor()

        self.__databases = databases
        self.__database = self.__conexion.info.dbname

        return self.__databases
    
    def refrescar_tablas(self):
        '''Extrae la tablas de la base de datos en la conexión actual.'''

        ### Validaciones:
        if not self.__conexion: raise ConnectionError("No hay conexión para extraer tablas.")

        ### Código:
        self.refrescar_cursor()
        self.__cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
        tablas:list[str] = [tb[0] for tb in self.__cursor.fetchall()]
        self.refrescar_cursor()

        self.__tablas = tablas
        self.__tabla = None
        # self.__tabla = self.__tablas[0]

        return self.__tablas
    
    def cambiar_database(self, db:str|int):
        '''Cambia de base de datos dentro de las disponibles en la conexión.'''

        ### Validaciones:
        if not isinstance(db, (str, int)): raise ValueError("La database solo puede ser seleccionada como 'str' o 'int'.")
        if not self.__databases: raise Exception("No hay bases de datos disponibles.")
        if not db in self.__databases: raise Exception(f"Base de datos no disponible\nBase de datos seleccionada:{db}\nBases de datos disponibles:{self.__databases}")

        ### Código:
        if isinstance(db, int): self.__database = self.__databases[db]
        else: self.__database = db

        self.__params["dbname"] = self.__database
        parametros = self.__params

        self.desconectarse()
        self.conectarse(**parametros)

    def cambiar_tabla(self, tbl:str|int):
        '''Cambia de base de datos dentro de las disponibles en la base de datos.'''

        ### Validaciones:
        if not isinstance(tbl, (str, int)): raise ValueError("La tabla solo puede ser seleccionada como 'str' o 'int'.")
        if not self.__tablas: raise Exception("No hay tablas disponibles.")
        if not tbl in self.__tablas: raise Exception(f"Tabla no disponible\nTabla seleccionada:{tbl}\nTablas disponibles:{self.__tablas}")

        ### Código:
        if isinstance(tbl, int): self.__tabla = self.__tablas[tbl]
        else: self.__tabla = tbl
        
    def obtener_columnas(self):
        '''Retorna una lista con las columnas de la tabla actualmente seleccionada en la clase.'''

        ### Validaciones:
        if not self.__tabla: raise AttributeError("No hay tabla sobre la que obtener columnas.")

        ### Código:
        self.refrescar_cursor()
        self.__cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
        """, ('public', self.__tabla))
        lista_columnas = [fila[0] for fila in self.__cursor.fetchall()]
        self.refrescar_cursor()

        return lista_columnas
    
    def obtener_filas(self):
        '''Retorna una lista de tuplas con las filas de la tabla actualmente seleccionada en la clase.'''

        ### Validaciones:
        if not self.__tabla: raise AttributeError("No hay tabla sobre la que obtener columnas.")

        ### Código:
        self.refrescar_cursor()
        self.__cursor.execute(f"SELECT * FROM {self.__tabla}")
        filas = self.__cursor.fetchall()
        self.refrescar_cursor()

        return filas