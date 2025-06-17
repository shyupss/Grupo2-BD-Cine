from . import tk, Tools

class ScrollableFrame(tk.Frame):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas=None, **kwargs):

        self.marco_contenedor:tk.Frame = tk.Frame(master)
        self.lienzo_dibujo:tk.Canvas = tk.Canvas(self.marco_contenedor)
        self.scrollbar_v:tk.Scrollbar = tk.Scrollbar(self.marco_contenedor, orient=tk.VERTICAL)
        self.scrollbar_h:tk.Scrollbar = tk.Scrollbar(self.marco_contenedor, orient=tk.HORIZONTAL)

        super().__init__(self.lienzo_dibujo, **kwargs)
        Tools.configurar_pesos(self.marco_contenedor, [1,0], [1,0])

        self.lienzo_dibujo.create_window((0, 0), window=self, anchor=tk.NW)
        self.lienzo_dibujo.bind("<Configure>", self.__actualizar_scrollregion)

        self.lienzo_dibujo.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_v.config(command=self.lienzo_dibujo.yview)

        self.lienzo_dibujo.configure(xscrollcommand=self.scrollbar_h.set)
        self.scrollbar_h.config(command=self.lienzo_dibujo.xview)

        self.lienzo_dibujo.grid(row=0, column=0, sticky=tk.NSEW)
        self.configurar_scrollbars_visibles(True, True)

    def grid(self, **kwargs):
        self.marco_contenedor.grid(**kwargs)

    def __actualizar_scrollregion(self, *_):
        '''Actualiza el canvas para que los scrollbars consideres el area scrolleable.'''
        self.lienzo_dibujo.configure(scrollregion=self.lienzo_dibujo.bbox("all"))

    def configurar_scrollbars_visibles(self, mostrar_scroll_v:bool = True, mostrar_scroll_h:bool = True):
        """Muestra u oculta los scrollbars según los parámetros."""
        if mostrar_scroll_v: self.scrollbar_v.grid(row=0, column=1, sticky=tk.NS)
        else: self.scrollbar_v.grid_remove()

        if mostrar_scroll_h: self.scrollbar_h.grid(row=1, column=0, sticky=tk.EW)
        else: self.scrollbar_h.grid_remove()