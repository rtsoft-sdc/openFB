import cv2
import logging
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class WarpPolar:
    
    @staticmethod
    def get_interpolation_flag(flag_str) -> int:
        clean_name = flag_str.strip().upper()
        base_flag = cv2.WARP_POLAR_LOG if "LOG" in clean_name else cv2.WARP_POLAR_LINEAR
        if "INVERSE" in clean_name or "INV" in clean_name:
            base_flag |= cv2.WARP_INVERSE_MAP
        return base_flag

    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, DSIZE, CENTER, MAXRADIUS, FLAGS):
        if event_input_name == "REQ":
            img = GlobalVideoMemory.pop(QUEUE_ID, IMG_ID)
            if img is not None:
                try:
                    dsize_tuple = (int(DSIZE[0]), int(DSIZE[1]))
                    center_tuple = (int(CENTER[0]), int(CENTER[1]))
                    flags_int = self.get_interpolation_flag(FLAGS)
                    warped_img = cv2.warpPolar(img, dsize_tuple, center_tuple, MAXRADIUS, flags_int)
                    GlobalVideoMemory.push(QUEUE_ID, IMG_ID, warped_img)
                    return event_input_value, IMG_ID, QUEUE_ID, "OK"
                except Exception as e:
                    logging.error(f"Error occurred while warping polar: {e}")
            logging.error(f"Image with ID {IMG_ID} not found in queue {QUEUE_ID}.")
            return event_input_value, IMG_ID, QUEUE_ID, "Image not found"

    def __del__(self):
        logging.info("Delete WarpPolar")