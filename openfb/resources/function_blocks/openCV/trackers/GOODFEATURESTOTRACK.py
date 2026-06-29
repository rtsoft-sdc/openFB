import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class GOODFEATURESTOTRACK():
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, MAXCORNERS, QUALITYLEVEL, MINDISTANCE, MASK, BLOCK_SIZE, GRADIENTSIZE, USE_HARRIS, K):
        if event_input_name == 'REQ':
            img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)
            if img is not None:
                if len(img.shape) == 3 and img.shape[2] == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                corners = cv2.goodFeaturesToTrack(img, MAXCORNERS, QUALITYLEVEL, MINDISTANCE, mask=MASK, blockSize=BLOCK_SIZE, gradientSize=GRADIENTSIZE, useHarrisDetector=USE_HARRIS, k=K)
                corners = corners[:, 0, 0].tolist() if corners is not None else []
                return event_input_value, "OK", IMG_ID, corners
            return event_input_value, "ERROR: no image found", None, None

    def __del__(self):
        pass