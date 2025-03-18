from abc import ABC, abstractmethod

from typing import Any


class DataLoaderBase(ABC):
    @abstractmethod
    def get_data(self, idx: int) -> Any:
        pass
    
    @abstractmethod
    def get_size(self) -> int:
        pass

    def __len__(self):
        return self.get_size()
