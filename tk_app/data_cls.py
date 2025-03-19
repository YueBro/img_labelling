import tkinter as tk
from dataclasses import dataclass

from typing import Any, Optional, List


@dataclass
class Widgets:
    win: tk.Tk
    img_displayer: tk.Label
    label_buttons: List[tk.Button]
    notify_bar: tk.Label
    jump_entry: tk.Entry
    jump_button: tk.Button


@dataclass
class Datas:
    storage_save_path: str


@dataclass
class LabelButtonInfo:
    label_str: str
    label_val: Any
    key_bind: Optional[str]=None
