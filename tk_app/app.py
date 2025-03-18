import tkinter as tk

from mods.data_storage import DataStorage
from .manager import Manager, Widgets
from .data_cls import LabelButtonInfo
from .cacher import Cacher

from typing import List


def start_app(data_storage: DataStorage, label_button_infos: List[LabelButtonInfo]):
    win = tk.Tk()
    win.resizable(False, False)
    
    upper_frm = tk.Frame(win, background="red")
    upper_frm.pack(side="top")
    # img_displayer = tk.Label(upper_frm, width=80, height=30, background="red")
    img_displayer = tk.Label(upper_frm, background="red")
    img_displayer.pack(side="left")
    buttons_frm = tk.Frame(upper_frm)
    buttons_frm.pack(side="right")
    buttons = []
    for lab_but_info in label_button_infos:
        txt = lab_but_info.label_str + ("" if (lab_but_info.key_bind is None) else f" <{lab_but_info.key_bind}>")
        button = tk.Button(buttons_frm, width=20, text=txt)
        button.pack(side="top")
        buttons.append(button)

    lower_frm = tk.Frame(win, background="blue")
    lower_frm.pack(side="top")
    notify_bar = tk.Label(lower_frm, width=100, height=1, background="orange", anchor="w")
    notify_bar.pack(side="left", fill='both')
    jump_button = tk.Button(lower_frm, text="jump")
    jump_button.pack(side="right", fill='both')
    jump_entry = tk.Entry(lower_frm)
    jump_entry.pack(side="right", fill='both')

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
