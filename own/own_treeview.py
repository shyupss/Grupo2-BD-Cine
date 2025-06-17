from . import tk, ttk, Tools

class Treeview(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master)
        Tools.configurar_pesos(self, [1, 0], [1, 0])

        # Canvas para permitir scroll horizontal real
        self.canvas = tk.Canvas(self)
        self.tree = ttk.Treeview(self.canvas, **kwargs)

        self.v_scroll = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.h_scroll = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.tree.configure(yscrollcommand=self.v_scroll.set)
        self.canvas.configure(xscrollcommand=self.h_scroll.set)

        # Embed el tree en el canvas
        self.tree_id = self.canvas.create_window((0, 0), window=self.tree, anchor='nw')

        # Bind para ajustar scroll horizontal cuando cambie el contenido
        self.tree.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._ajustar_treeview)

        # Layout
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.v_scroll.grid(row=0, column=1, sticky=tk.NS)
        self.h_scroll.grid(row=1, column=0, sticky=tk.EW)

    def _ajustar_treeview(self, event:tk.Event):
        canvas_width = event.width
        canvas_height = event.height
        self.canvas.itemconfigure(self.tree_id, width=canvas_width, height=canvas_height)

    # Métodos delegados
    def definir_columnas(self, cols, anchos=None):
        self.tree["columns"] = cols
        self.tree["show"] = "headings"
        for i, c in enumerate(cols):
            w = anchos[i] if anchos and i < len(anchos) else 100
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)

    def definir_filas(self, filas):
        for f in filas: self.tree.insert('', tk.END, values=f)

    def limpiar(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.tree["columns"] = []
