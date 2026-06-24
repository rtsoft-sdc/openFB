# need to add ogl support 

import cv2
import logging
import tkinter as tk
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory

class Imshow:
    def __init__(self):
        self.window_size = (800, 600)
        self.root = None
        self.label = None
        self.window_is_open = False
        
    def _on_close(self):
        self.window_is_open = False
        if self.root:
            self.root.destroy()
            self.root = None
            self.label = None
        
    def schedule(self, event_input_name, event_input_value, IMG_ID, QUEUE_ID, WINDOW_NAME):
        if event_input_name == 'INIT':
            try:
                if self.root is not None:
                    self.root.destroy()
                    
                self.root = tk.Tk()
                self.root.title(WINDOW_NAME)
                self.root.geometry(f"{self.window_size[0]}x{self.window_size[1]}")
                self.root.protocol("WM_DELETE_WINDOW", self._on_close)
                
                self.label = tk.Label(self.root, bg="black")
                self.label.pack(expand=True, fill=tk.BOTH)
                
                self.window_is_open = True
                
                self.root.update_idletasks()
                self.root.update()

                self.root.mainloop()

                return None, event_input_value, True, None, None, "Window initialized successfully."
            except Exception as e:
                return None, event_input_value, False, None, None, "Failed to initialize window."

        elif event_input_name == 'REQ':
                if self.root is None or not self.window_is_open:
                    return event_input_value, None, False, None, None, "Window is not initialized or has been closed."

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
                                
                            self.window_is_open = True
                            return event_input_value, None, True, IMG_ID, QUEUE_ID, "Image displayed successfully."
                        else:
                            return event_input_value, None, False, None, None, "Window has been closed."
                    except Exception as e:
                        return event_input_value, None, False, None, None, "Failed to display image."
        else:
            return event_input_value, None, False, None, None, "Unknown event input name."
    def __del__(self):
        logging.info('Stopping Imshow')
        if self.root:
            try:
                self.root.destroy()
            except Exception as e:
                logging.error(f"Failed to destroy window: {e}")
                pass
    