from abc import ABC, abstractmethod
from typing import Any, Optional

class AbstractChannel(ABC):
    
    @abstractmethod
    def read_data(self, address, datatype):
        pass
    
    @abstractmethod
    def write_data(self, address, value, datatype) -> bool:
        pass
    
    @abstractmethod
    def parse_IO_params(self, params):
        pass
    
    @abstractmethod
    def stop(self) -> None:
        pass