import tkinter as tk
from dataclasses import dataclass

from mods.data_storage import DataStorage
from .data_cls import Widgets, LabelButtonInfo, Datas
from .widget_opers import refresh_img
from .cacher import Cacher

from typing import List, Tuple, Optional, Any


_DISALLOWED_STATES = 0b100000000000000101  # alt, ctrl, shift
_ALLOWED_KEYS = set("abcdefghijklmnopqrstuvwxyz0123456789")
_ARROW_KEYS = set(["left", "right"])
_DIGITS = set("0123456789")


@dataclass
class _Stat:
    win_size: Tuple[int, int]

    display_idx: int=0
    need_refresh: bool=False


class Manager:
    def __init__(self, data_storage: DataStorage, label_button_infos: List[LabelButtonInfo], widgets: Widgets,
                 datas: Datas, cacher: Cacher):
        for lab_but_info in label_button_infos:
            if (lab_but_info.key_bind is not None) and (lab_but_info.key_bind not in _ALLOWED_KEYS):
                raise KeyError(f"{lab_but_info.key_bind.__repr__()} cannot be used as the shortcut key.")
        self.label_button_infos = label_button_infos
        self.data_storage = data_storage
        self.wgs = widgets
        self.cacher = cacher
        self.datas = datas

        jumper_vcmd = (widgets.jump_entry.register(self._validcmd_jumper), '%S')
        widgets.jump_entry.config(validate="key", validatecommand=jumper_vcmd)

        self.stat = _Stat(
            win_size=(widgets.win.winfo_height(), widgets.win.winfo_width()),
            display_idx=0,
            need_refresh=False,
        )
        self._refresh(forced=True)

    def recall_key_press(self, event: tk.Event):
        state = event.state
        key = event.keysym.lower()
        if event.send_event != True:
            return
        if (not isinstance(state, int)) or ((state & _DISALLOWED_STATES) != 0):
            return
        if key not in (_ALLOWED_KEYS | _ARROW_KEYS):
            return
        # print(event, bin(state), key)
        self._update_label_on_key_press(key)
        self._change_idx_on_key_press(key)
        self._refresh()

    def recall_key_release(self, event: tk.Event):
        # key = event.keysym.lower()
        # print(event, key)
        pass

    def recall_window_config(self, event: tk.Event):
        new_size = (self.wgs.win.winfo_height(), self.wgs.win.winfo_width())
        if new_size != self.stat.win_size:
            self.stat.win_size = new_size
            self._refresh(forced=True)
        # print(event, self.stat.win_size)
    
    def recall_jump_button_press(self):
        try:
            jump_idx = int(self.wgs.jump_entry.get()) - 1
            self.stat.display_idx = min(max(jump_idx, 0), len(self.data_storage) - 1)
            self.wgs.jump_entry.delete(0, 'end')
            self._refresh(forced=True)
        except ValueError:
            self._update_notification("ERROR!")

    def _update_label_on_key_press(self, key: str):
        for info in self.label_button_infos:
            if key == info.key_bind:
                self.data_storage.set_label(self.stat.display_idx, info.label_val)
                self.stat.need_refresh = True
                self.data_storage.save(self.datas.storage_save_path)
                break

    def _refresh(self, forced=False):
        if (forced is False) and (self.stat.need_refresh is False):
            return

        has_label, img_path, label = self.data_storage.get_info(self.stat.display_idx)
        label_idx = self._find_button_idx_by_label_val(label)
        img_max_size = (self.wgs.img_displayer.winfo_width(), self.wgs.img_displayer.winfo_height())

        refresh_img(self.wgs.img_displayer, img_path, self.cacher, "display_image", img_max_size)
        self._highlight_button(label_idx)
        self._update_notification()

        self.stat.need_refresh = False

    def _highlight_button(self, button_idx: Optional[int]):
        for button in self.wgs.label_buttons:
            button.config(fg="#000000")
        if button_idx is not None:
            self.wgs.label_buttons[button_idx].config(fg="#ff7000")

    def _change_idx_on_key_press(self, key: str):
        if key not in _ARROW_KEYS:
            return
        if key == "right":
            self.stat.display_idx = min(self.stat.display_idx + 1, len(self.data_storage) - 1)
        elif key == "left":
            self.stat.display_idx = max(self.stat.display_idx - 1, 0)
        self.stat.need_refresh = True

    def _find_button_idx_by_label_val(self, label_val: Any) -> Optional[int]:
        for label_idx,  lab_but_info in enumerate(self.label_button_infos):
            if lab_but_info.label_val == label_val:
                return label_idx
        return None

    def _update_notification(self, extra_str: Optional[str]=None):
        has_label, img_path, label = self.data_storage.get_info(self.stat.display_idx)
        txt = f"[{self.stat.display_idx+1}/{len(self.data_storage)}] {img_path}"
        if extra_str is not None:
            txt += " | " + extra_str
        self.wgs.notify_bar.config(text=txt)

    def _validcmd_jumper(self, s: str):
        return all((c in _DIGITS) for c in s)
