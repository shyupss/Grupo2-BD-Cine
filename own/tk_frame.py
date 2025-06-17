from . import tk

class Frame(tk.Frame):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas, **kwargs):
        super().__init__(master, **kwargs)