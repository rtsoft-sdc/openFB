import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class IMREAD:
    def schedule(self, event_input_name, event_input_value, QI, QUEUE_ID, FILE_PATH):
        if event_input_name == 'REQ' and QI:
            try:
                img = cv2.imread(FILE_PATH)
                if img is not None:
                    queue_id = GlobalVideoMemory.get_queue_id(QUEUE_ID)
                    last_img_id = GlobalVideoMemory.get_last_img_id(queue_id)
                    new_img_id = last_img_id + 1 if last_img_id is not None else 0
                    GlobalVideoMemory.set(queue_id, img_id=new_img_id, frame=img)
                    return event_input_value, True, "OK", new_img_id 
                else:
                    return event_input_value, False, "ERROR: could not read image", None
            except Exception as e:
                return event_input_value, False, "ERROR: " + str(e), None