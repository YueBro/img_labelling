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
        self.paths.sort()

    def get_data(self, idx: int) -> Any:
        return self.paths[idx]
    
    def get_size(self) -> int:
        return len(self.paths)


dataloader = MyDataLoader(r"E:\images", do_recursive=True, filter_fn=lambda p: p.endswith(".jpg"))
data_storage = DataStorage(dataloader)

start_app(data_storage, [
    LabelButtonInfo("左变道", 1, 'u'),
    LabelButtonInfo("保持车道", 2, 'i'),
    LabelButtonInfo("右变道", 3, 'o'),
    LabelButtonInfo("左转", 4, 'j'),
    LabelButtonInfo("直行", 5, 'k'),
    LabelButtonInfo("右转", 6, 'l'),
    LabelButtonInfo("掉头", 7, 'm'),
])
