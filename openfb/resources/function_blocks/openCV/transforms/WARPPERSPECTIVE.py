import cv2
import numpy as np
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class WARPPERSPECTIVE:
    
    border_methods = (
        cv2.BORDER_CONSTANT,
        cv2.BORDER_REPLICATE,
        cv2.BORDER_REFLECT,
        cv2.BORDER_WRAP,
        cv2.BORDER_REFLECT_101,
        cv2.BORDER_TRANSPARENT,
        cv2.BORDER_REFLECT101,
        cv2.BORDER_DEFAULT,
        cv2.BORDER_ISOLATED
    )
    
    def get_border_type(self, border_type: int) -> int:
        return self.border_methods[border_type] if 0 <= border_type < len(self.border_methods) else cv2.BORDER_DEFAULT

    
    interpolation_methods = (
        cv2.INTER_NEAREST,
        cv2.INTER_LINEAR,
        cv2.INTER_CUBIC,
        cv2.INTER_AREA,
        cv2.INTER_LANCZOS4,
        cv2.INTER_LINEAR_EXACT,
        cv2.INTER_NEAREST_EXACT,
        cv2.INTER_MAX,
        cv2.WARP_FILL_OUTLIERS,
        cv2.WARP_INVERSE_MAP,
        cv2.WARP_RELATIVE_MAP
    ) 
    
    def get_interpolation_method(self, interpolation_method: int) -> int:
        return self.interpolation_methods[interpolation_method] if 0 <= interpolation_method < len(self.interpolation_methods) else cv2.INTER_LINEAR

    def schedule(
        self,
        event_input_name,
        event_input_value,
        QUEUE_ID,
        IMG_ID,
        TRANSFORMATION_MATRIX,
        DSIZE, FLAGS, BORDERMODE, BORDERVALUE
    ):
        if event_input_name == "REQ":
            img = GlobalVideoMemory.get(QUEUE_ID, IMG_ID)
            if img is not None:
                try:
                    map = np.array(TRANSFORMATION_MATRIX, dtype=np.float32).reshape((3, 3))
                    dsize = (DSIZE[0], DSIZE[1])
                    
                    img = cv2.warpPerspective(img, M=map, dsize=dsize, flags=self.get_interpolation_method(FLAGS), borderMode=self.get_border_type(BORDERMODE), borderValue=BORDERVALUE)
                    GlobalVideoMemory.set(QUEUE_ID, IMG_ID, img)
                    return event_input_value, "OK", IMG_ID
                except Exception as e:
                    return event_input_value, "ERROR: Failed to warp perspective", None
            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass