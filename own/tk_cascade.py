from . import tk

import tkinter as tk

class Cascade(tk.Frame):
    def __init__(self, master=None, opciones=None, **kwargs):
        super().__init__(master, **kwargs)
        self.opciones = opciones if opciones else {}
        
        self.boton = tk.Menubutton(self, text="Menú", relief=tk.RAISED, direction="below")
        self.menu = tk.Menu(self.boton, tearoff=0)
        self.boton.config(menu=self.menu)

        self._crear_menu(self.menu, self.opciones)

        self.boton.pack()

    def _crear_menu(self, menu, opciones):
        for etiqueta, valor in opciones.items():
            if isinstance(valor, dict):
                submenu = tk.Menu(menu, tearoff=0)
                self._crear_menu(submenu, valor)
                menu.add_cascade(label=etiqueta, menu=submenu)
            else:
                menu.add_command(label=etiqueta, command=valor)
