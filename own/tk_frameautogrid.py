from . import tk

class FrameAutoGrid(tk.Frame):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas = None, posiciones:dict[tk.Widget,list[tuple[int,int]]] = None, **kwargs):
        '''tk.Frame en el que puedes posicionar multiples Widgets rapidamente a través de un estructura de la forma 'dict[tk.Widget,list[tuple[int,int]]]'.'''
        if not posiciones or not isinstance(posiciones, dict): raise ValueError("El parámetro 'posiciones' debe ser un diccionario no vacío.")

        self.__widgets:dict[tuple[int,int],tk.Widget] = {}

        super().__init__(master, **kwargs)

        for wdg, pos_list in posiciones.items():
            for row, col in pos_list:
                widget = wdg(self)
                widget.grid(row=row, column=col)
                self.__widgets[(row, col)] = widget

    @property
    def widgets(self):
        return self.__widgets