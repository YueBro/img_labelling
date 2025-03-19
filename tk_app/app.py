import tkinter as tk

from mods.data_storage import DataStorage
from .manager import Manager, Widgets
from .data_cls import LabelButtonInfo
from .cacher import Cacher
from .consts import BUTTONS_WIDTH

from typing import List, Tuple


def start_app(data_storage: DataStorage, label_button_infos: List[LabelButtonInfo],
              win_size: Tuple[int, int]=(1200, 800)):
    win = tk.Tk()
    win.geometry(f"{win_size[0]}x{win_size[1]}")
    # win.resizable(False, False)

    upper_frm = tk.Frame(win, background="red")
    upper_frm.place(x=0, y=0, relheight=1.0, height=-30, relwidth=1.0)
    img_displayer = tk.Label(upper_frm, background="red")
    img_displayer.place(x=0, y=0, relheight=1.0, relwidth=1.0, width=-BUTTONS_WIDTH)
    buttons_frm = tk.Frame(upper_frm)
    buttons_frm.place(relx=1.0, x=-BUTTONS_WIDTH, y=0, relheight=1.0, width=BUTTONS_WIDTH)
    buttons = []
    for lab_but_info in label_button_infos:
        txt = lab_but_info.label_str + ("" if (lab_but_info.key_bind is None) else f" <{lab_but_info.key_bind}>")
        button = tk.Button(buttons_frm, text=txt)
        button.pack(side="top", fill='x')
        buttons.append(button)

    lower_frm = tk.Frame(win, background="blue")
    lower_frm.place(x=0, rely=1.0, y=-30, height=30)
    notify_bar = tk.Label(lower_frm, width=win_size[0], height=1, background="orange", anchor="w")
    notify_bar.pack(side="left", fill='both')
    jump_button = tk.Button(lower_frm, text="jump")
    jump_button.pack(side="right", fill='both')
    jump_entry = tk.Entry(lower_frm)
    jump_entry.pack(side="right", fill='both')

    win.update()  # widget's sizes can obtain after win.update()
    wgs = Widgets(
        win=win,
        img_displayer=img_displayer,
        label_buttons=buttons,
        notify_bar=notify_bar,
        jump_entry=jump_entry,
        jump_button=jump_button,
    )
    cacher = Cacher(win)
    mgr = Manager(data_storage, label_button_infos, wgs, cacher)
    win.bind("<KeyPress>", mgr.recall_key_press)
    win.bind("<KeyRelease>", mgr.recall_key_release)
    win.bind("<Configure>", mgr.recall_window_config)  # trigger when move or resize window
    jump_button.config(command=mgr.recall_jump_button_press)
    tk.mainloop()
