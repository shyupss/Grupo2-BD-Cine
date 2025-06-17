from . import tk

from tkinter.scrolledtext import ScrolledText

class TextFrame(ScrolledText):

    def __init__(self, master:tk.Tk|tk.Toplevel|tk.Frame|tk.Canvas, **kwargs):
        super().__init__(master, **kwargs)