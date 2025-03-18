import tkinter as tk

from .cacher import Cacher

from PIL import Image, ImageTk

from typing import Optional, Tuple


def _get_hw_to_constraint(hw: Tuple[int, int], constraint_hw: Tuple[int, int]):
    h_scale = constraint_hw[0] / hw[0]
    w_scale = constraint_hw[1] / hw[1]
    scale = min(h_scale, w_scale)
    return round(hw[0] * scale), round(hw[1] * scale)


def refresh_img(tk_label: tk.Label, img_path: str, cacher: Cacher, cache_key: str,
                constraint_hw: Optional[Tuple[int, int]]=None):
    pil_im = Image.open(img_path)
    if constraint_hw is not None:
        new_hw = _get_hw_to_constraint((pil_im.width, pil_im.height), constraint_hw)
        pil_im = pil_im.resize(new_hw)
    tk_im = ImageTk.PhotoImage(pil_im)
    cacher[cache_key] = tk_im
    tk_label.config(image=tk_im)
