import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class WARPPOLAR:
    
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
    
    warp_polar_modes = (
        cv2.WARP_POLAR_LINEAR,
        cv2.WARP_POLAR_LOG
    )
    
    def get_result_flag(self, interpolation_flag: int, warp_polar_flag: int) -> int:
        interpolation_method = self.interpolation_methods[interpolation_flag] if 0 <= interpolation_flag < len(self.interpolation_methods) else cv2.INTER_LINEAR
        warp_polar_method = self.warp_polar_modes[warp_polar_flag] if 0 <= warp_polar_flag < len(self.warp_polar_modes) else cv2.WARP_POLAR_LINEAR
        return interpolation_method | warp_polar_method

    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, DSIZE, CENTER, MAXRADIUS, FLAGS):
        if event_input_name == "REQ":
            img = GlobalVideoMemory.get(QUEUE_ID, IMG_ID)
            if img is not None:
                try:
                    dsize_tuple = (int(DSIZE[0]), int(DSIZE[1]))
                    center_tuple = (int(CENTER[0]), int(CENTER[1]))
                    flags_int = self.get_result_flag(FLAGS[0], FLAGS[1])
                    warped_img = cv2.warpPolar(img, dsize_tuple, center_tuple, MAXRADIUS, flags_int)
                    GlobalVideoMemory.set(QUEUE_ID, IMG_ID, warped_img)
                    return event_input_value, "OK", IMG_ID
                except Exception as e:
                    return event_input_value, "ERROR: Failed to warp polar", None
                
            return event_input_value, "ERROR: Image not found", None

    def __del__(self):
        pass