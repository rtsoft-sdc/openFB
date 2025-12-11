from abc import ABC, abstractmethod

class BaseSync(ABC):
    
    @abstractmethod
    def synchronize(self):
        pass

    @abstractmethod
    def wipe(self):
        pass
