from . import tk

class Widget(tk.Widget):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas, **kwargs):
        super().__init__(master, **kwargs)