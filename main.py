import os
import os.path as osp

from mods.data_loader import DataLoaderBase
from mods.data_storage import DataStorage
from tk_app import start_app
from tk_app.data_cls import LabelButtonInfo

from typing import Any, Callable, Optional, List


class MyDataLoader(DataLoaderBase):
    def __init__(self, imgs_root: str, do_recursive=False, filter_fn: Optional[Callable[..., bool]]=None):
        self.paths: List[str] = []
        for rt, _, filenames in os.walk(imgs_root):
            for filename in filenames:
                path = osp.join(rt, filename)
                if (filter_fn is not None) and (filter_fn(path) is False):
                    continue
                self.paths.append(path)
            if not do_recursive:
                break
        if len(self.paths) == 0:
            raise RuntimeError(f"No data found!")
        self.paths.sort()

    def get_data(self, idx: int) -> Any:
        return self.paths[idx]
    
    def get_size(self) -> int:
        return len(self.paths)


LABEL_RESULT: Optional[str] = r"D:\Downloads\新建文件夹 (2)\manual_label_result.pkl"

if (LABEL_RESULT is None) or (not osp.exists(LABEL_RESULT)):
    dataloader = MyDataLoader(r"D:\Downloads\新建文件夹 (2)\可视化-基线", do_recursive=True, filter_fn=lambda p: p.endswith(".jpg"))
    data_storage = DataStorage(dataloader)
else:
    data_storage = DataStorage.load(LABEL_RESULT)

label_button_infos = [
    LabelButtonInfo("左变道", 1, 'u'),
    LabelButtonInfo("保持车道", 2, 'i'),
    LabelButtonInfo("右变道", 3, 'o'),
    LabelButtonInfo("左转", 4, 'j'),
    LabelButtonInfo("直行", 5, 'k'),
    LabelButtonInfo("右转", 6, 'l'),
    LabelButtonInfo("掉头", 7, 'm'),
]

start_app(data_storage, label_button_infos, LABEL_RESULT)
