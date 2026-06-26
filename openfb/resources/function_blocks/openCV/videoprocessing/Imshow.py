# need to add ogl support 

import cv2
import tkinter as tk
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class Imshow:
    
    def __init__(self):
        self.root = tk.Tk()
        self.title = "Waiting for Image"
        self.root.title(self.title)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.label = tk.Label(self.root, bg="black")
        self.label.pack(expand=True, fill=tk.BOTH)
        
        self.root.update_idletasks()
        self.root.update()

        self.window_is_open = True
                
    def _on_close(self):
        self.window_is_open = False
        if self.root:
            self.root.destroy()
        
    
        
    def schedule(self, event_input_name, event_input_value, QUEUE_ID, IMG_ID, WINDOW_NAME):
        if event_input_name == 'REQ':
                if self.root is None or not self.window_is_open:
                    return event_input_value, None, False, None, None, "Window is not initialized or has been closed."
                if self.title != WINDOW_NAME:
                    self.title = WINDOW_NAME
                    self.root.title(self.title)
                img = GlobalVideoMemory.pop(queue_id=QUEUE_ID, img_id=IMG_ID)
                if img is not None:
                    try:
                        if self.root.winfo_exists() == 1:
                            
                            if len(img.shape) == 3 and img.shape[2] == 3:
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            
                            success, encoded_image = cv2.imencode('.ppm', img)
                            if not success:
                                return event_input_value, None, False, None, None, "Failed to encode image for display."
                            tk_img = tk.PhotoImage(data=encoded_image.tobytes())
                            self.label.config(image=tk_img)
                            self.label.image = tk_img
                            self.root.update_idletasks()
                            self.root.update()
                            
                            return event_input_value, None, True, IMG_ID, QUEUE_ID, "Image displayed successfully."
                        else:
                            return event_input_value, None, False, None, None, "Window has been closed."
                    except Exception as e:
                        return event_input_value, None, False, None, None, "Failed to display image."


    def __del__(self):
        if self.root:
            try:
                self.root.destroy()
            except Exception as e:
                pass
    