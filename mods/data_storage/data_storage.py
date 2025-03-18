from __future__ import annotations

import pickle as pkl

from mods.data_loader import DataLoaderBase

from typing import Sequence, Optional, Any, Tuple


class _PseudoDataLoader(DataLoaderBase):
    def get_data(self, idx: int) -> Any:
        return None
    
    def get_size(self) -> int:
        return 0


class DataStorage:
    def __init__(self, data_loader: DataLoaderBase, labels_info: Optional[Sequence[Tuple[int, Any]]]=None):
        self.data_loader = data_loader                # data loader
        self.labels = [None] * len(data_loader)       # label
        self.label_flag = [False] * len(data_loader)  # whether is labeled
        if labels_info is not None:
            self.set_multi_labels(labels_info)

    @staticmethod
    def load(path: str) -> DataStorage:
        with open(path, "rb") as fp:
            var = pkl.load(fp)
        new_data_storage = DataStorage(_PseudoDataLoader())
        new_data_storage.data_loader = var["data_loader"]
        new_data_storage.labels = var["labels"]
        new_data_storage.label_flag = var["label_flag"]
        return new_data_storage

    def save(self, path: str):
        with open(path, "wb") as fp:
            pkl.dump({
                "data_loader": self.data_loader,
                "labels": self.labels,
                "label_flag": self.label_flag,
            }, fp)

    def get_info(self, idx: int) -> Tuple[bool, Any, Any]:
        return self.label_flag[idx], self.data_loader.get_data(idx), self.labels[idx]

    def set_label(self, idx: int, label: Any):
        self.labels[idx] = label
        self.label_flag[idx] = True

    def set_multi_labels(self, labels_info: Sequence[Tuple[int, Any]]):
        for idx, label in labels_info:
            self.labels[idx] = label
            self.label_flag[idx] = True

    def __len__(self):
        return len(self.data_loader)
