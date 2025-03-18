import tkinter as tk


class Cacher:
    def __init__(self, win: tk.Tk):
        self.win = win
        self.disallowed_keys = set(dir(win))
    
    def __setitem__(self, other: str, val):
        if other in self.disallowed_keys:
            raise KeyError(f"Key {other} occupied!")
        setattr(self.win, other, val)
