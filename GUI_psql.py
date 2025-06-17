import own
from own.own_treeview import Treeview

BTN_CONECT = "Conectarse"
BTN_DESCON = "Desconectarse"

class GUIpsql(own.Tk):

    def __init__(self, *args, **kwargs):
        self.conexion = own.PgConnect()
        self.conexion.verbose = (False, True)

        super().__init__(*args, **kwargs)
        own.Tools.configurar_pesos(self, [1, 1, 1, 1], [1, 0])

        self.treeview = Treeview(self)
        self.treeview.grid(row=0, column=0, sticky=own.NSEW, rowspan=4)

        self.inicio_sesion = own.FrameLabel(self)
        own.Tools.configurar_pesos(self.inicio_sesion, [0, 0], {1})
        self.inicio_sesion.texto = "Conectarse a PostgresSQL:"
        self.inicio_sesion.grid(row=0, column=1, sticky=own.NSEW)

        self.datos_conexion = own.FrameAutoGrid(self.inicio_sesion, {
            own.Label:[(0,0),(1,0),(2,0),(3,0),(4,0)],
            own.Entry:[(0,1),(1,1),(2,1),(3,1),(4,1)],
        })
        
        for i, etiqueta in enumerate(["Usuario:", "Constraseña:", "Host:", "Puerto:", "Base de Datos:"]):
            self.datos_conexion.widgets[(i,0)].texto = etiqueta
            self.datos_conexion.widgets[(i,0)].grid_configure(sticky=own.E)

        self.datos_conexion.widgets[(2,1)].texto = own.DEF_HOST if own.DEF_HOST else ""
        self.datos_conexion.widgets[(3,1)].texto = own.DEF_PORT if own.DEF_PORT else ""
        self.datos_conexion.widgets[(4,1)].texto = own.DEF_DBNAME if own.DEF_DBNAME else ""

        self.datos_conexion.grid(row=0, column=0, sticky=own.NSEW)

        self.boton_conexion = own.Button(self.inicio_sesion)
        self.boton_conexion.texto = BTN_CONECT
        self.boton_conexion.exe_boton = self.__exe_conectar
        self.boton_conexion.grid(row=1, column=0, sticky=own.NSEW)

        self.seleccionar_database_frame = own.FrameLabel(self)
        own.Tools.configurar_pesos(self.seleccionar_database_frame, [0], [1])
        self.seleccionar_database_frame.texto = "Selecciona base de dato:"
        self.seleccionar_database_frame.grid(row=1, column=1, sticky=own.NSEW)

        self.seleccionar_database = own.Menubutton(self.seleccionar_database_frame, default=("No hay Bases de Datos.", None))
        self.seleccionar_database.grid(row=0, column=0, sticky=own.EW)

        self.seleccionar_tabla_frame = own.FrameLabel(self)
        own.Tools.configurar_pesos(self.seleccionar_tabla_frame, [0], [1])
        self.seleccionar_tabla_frame.texto = "Seleccionar tabla:"
        self.seleccionar_tabla_frame.grid(row=2, column=1, sticky=own.NSEW)

        self.seleccionar_tabla = own.Menubutton(self.seleccionar_tabla_frame, default=("No hay Tablas disponibles.", None))
        self.seleccionar_tabla.grid(row=0, column=0, sticky=own.EW)

        self.crud_frame = own.FrameLabel(self)
        own.Tools.configurar_pesos(self.crud_frame, [0, 0, 0, 0], [1])
        self.crud_frame.texto = "CRUD:"
        self.crud_frame.grid(row=3, column=1, sticky=own.NSEW)

        self.crud_create = own.Button(self.crud_frame)
        self.crud_create.texto = "Insertar Dato"
        self.crud_create.grid(row=0, column=0, sticky=own.EW)

        self.crud_read = own.Button(self.crud_frame)
        self.crud_read.texto = "Leer Dato (?)"
        self.crud_read.grid(row=1, column=0, sticky=own.EW)

        self.crud_update = own.Button(self.crud_frame)
        self.crud_update.texto = "Modificar Dato"
        self.crud_update.grid(row=2, column=0, sticky=own.EW)

        self.crud_delete = own.Button(self.crud_frame)
        self.crud_delete.texto = "Borrar Dato"
        self.crud_delete.grid(row=3, column=0, sticky=own.EW)        

    def __estado_conectado(self):
        '''Pone el estado de los widgets de la app como si estuviese desconectado.'''
        self.update_idletasks()
        for _, widget in self.datos_conexion.widgets.items():
            if isinstance(widget, own.Entry): widget.config(state=own.DISABLED)

        self.boton_conexion.texto = BTN_DESCON
        self.boton_conexion.exe_boton = self.__exe_deconectar

        dbs = self.conexion.databases
        self.seleccionar_database.opciones = {tag:None for tag in dbs}
        self.seleccionar_database.exe_opcion = self.__seleccionar_db

        db = self.conexion.database
        self.seleccionar_database.opcion = db

        tbs = self.conexion.tablas
        self.seleccionar_tabla.opciones = {tag:None for tag in tbs}
        self.seleccionar_tabla.exe_opcion = self.__seleccionar_tb

        self.treeview.limpiar()

        self.update_idletasks()
        self.__seleccionar_db()
            

    def __estado_desconectado(self):
        '''Pone el estado de los widgets de la app como si estuviese desconectado.'''
        self.update_idletasks()
        for _, widget in self.datos_conexion.widgets.items():
            if isinstance(widget, own.Entry): widget.config(state=own.NORMAL)

        self.boton_conexion.texto = BTN_CONECT
        self.boton_conexion.exe_boton = self.__exe_conectar

        self.seleccionar_database.opciones = {}
        self.seleccionar_tabla.opciones = {}
        self.treeview.limpiar()

    def __exe_conectar(self, *_):
        host = self.datos_conexion.widgets[(2,1)].texto
        port = self.datos_conexion.widgets[(3,1)].texto
        dbname = self.datos_conexion.widgets[(4,1)].texto

        conectado = self.conexion.conectarse(
            user = self.datos_conexion.widgets[(0,1)].texto,
            password = self.datos_conexion.widgets[(1,1)].texto,
            host = host if host else own.DEF_HOST,
            port = port if port else own.DEF_PORT,
            dbname = dbname if dbname else own.DEF_DBNAME
        )

        if conectado: self.__estado_conectado()
        else: self.__estado_desconectado()

    def __exe_deconectar(self, *_):
        self.conexion.desconectarse()
        self.__estado_desconectado()

    def __seleccionar_db(self, *_):
        self.conexion.cambiar_database(self.seleccionar_database.opcion)

        tbs = self.conexion.tablas
        self.seleccionar_tabla.opciones = {tag:None for tag in tbs}

        if self.conexion.tablas:
            self.seleccionar_tabla.opcion = self.conexion.tablas[0]
            self.__seleccionar_tb()

    def __seleccionar_tb(self, *_):
        self.conexion.cambiar_tabla(self.seleccionar_tabla.opcion)

        columnas = self.conexion.obtener_columnas()
        filas = self.conexion.obtener_filas()

        self.treeview.limpiar()
        self.treeview.definir_columnas(columnas)
        self.treeview.definir_filas(filas)

programa = GUIpsql()
programa.title("CRUD (Solo Gráficos)")
own.Tools.configurar_pesos(programa, [1], [1])

programa.update_idletasks()
programa.geometry(f"{int(programa.winfo_width()*1.5)}x{int(programa.winfo_height())}")

programa.mainloop()