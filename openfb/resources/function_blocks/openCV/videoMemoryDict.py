import cv2
import numpy as np
import openfb.resources.function_blocks.openCV.CVsettings as CVsettings
from multiprocessing import shared_memory

class VideoSharedMemory():
    
    _instances = {}
    
    @classmethod
    def connect(cls, name, size):
        if name not in cls._instances:
            cls._instances[name] = cls(name, size)
        return cls._instances[name]
    
    def __init__(self, name, size):
        self.name = name
        self.shape = (CVsettings.IMAGE_HEIGHT, CVsettings.IMAGE_WIDTH, CVsettings.IMAGE_CHANNELS)
        self.dtype = np.uint8
        self.frame_size = np.prod(self.shape) * np.dtype(self.dtype).itemsize
        
        try:
            self.shm = shared_memory.SharedMemory(name=self.name)
        except FileNotFoundError:
            self.shm = shared_memory.SharedMemory(name=self.name, create=True, size=self.frame_size)
 
        self.buffer = self.shm.buf
            
    def get_frame(self, idx: int):
        offset = idx * self.frame_size
        return np.ndarray(self.shape, dtype=self.dtype, buffer=self.shm.buf, offset=offset)
    
    def write_frame(self, idx: int, img: np.ndarray):
        offset = idx * self.frame_size
        dst = np.ndarray(self.shape, dtype=self.dtype, buffer=self.shm.buf, offset=offset)
        np.copyto(dst, img)
    
    def close(self):
        self.shm.close()