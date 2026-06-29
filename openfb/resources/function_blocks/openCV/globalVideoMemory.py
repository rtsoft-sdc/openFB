import numpy as np

class GlobalVideoMemory():
    
    _storage = {}
    
    @classmethod
    def set(cls, queue_id: str, img_id: int, frame: np.ndarray):
        if queue_id not in cls._storage:
            cls._storage[queue_id] = {}
        cls._storage[queue_id][img_id] = frame
        MAX_FRAMES = 50
        if len(cls._storage[queue_id]) > MAX_FRAMES:
            first_key = next(iter(cls._storage[queue_id]))
            del cls._storage[queue_id][first_key]
    
    @classmethod
    def get(cls, queue_id: str, img_id: int) -> np.ndarray:
        return cls._storage.get(queue_id, {}).get(img_id)
    
    @classmethod
    def clear_queue(cls, queue_id: str):
        if queue_id in cls._storage:
            cls._storage[queue_id].clear()