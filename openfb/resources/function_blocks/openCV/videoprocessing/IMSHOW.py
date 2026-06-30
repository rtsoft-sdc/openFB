import cv2
from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
import queue
import tkinter as tk
import threading


class IMSHOW:
    
    def __init__(self):
        self.title = "Waiting for Image"
        self.window_is_open = True
        self.frame_queue = queue.Queue()
        self.last_frame = None
        self.root = None
        self.label = None
        self.run_display_thread = threading.Thread(target=self.init_window, daemon=True)
        self.run_display_thread.start()
    
    
    def init_window(self):
        try:
            self.root = tk.Tk()
            self.root.title(self.title)
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.label = tk.Label(self.root, text="Waiting...")
            self.label.pack(expand=True, fill=tk.BOTH)
            self.window_is_open = True
            self.root.after(1000, self.check_queue)
        except Exception as e:
            with open("/tmp/IMSHOW_error.log", "a") as f:
                f.write(f"Error Tkinter: {e}\n")
        self.root.mainloop()
        
    def on_close(self):
        self.window_is_open = False
        if self.root is not None:
            self.root.destroy()
    
    def check_queue(self):
        if not self.window_is_open or self.root is None:
            return
        
        frame = None
        try:
            frame = self.frame_queue.get()
        except queue.Empty:
            pass
        if frame is not None:
            try:
                image = GlobalVideoMemory.get(queue_id=frame[0], img_id=frame[1])
                if image is not None:
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    success, encoded_img = cv2.imencode('.ppm', rgb_image)
                    if success:
                        tk_img = tk.PhotoImage(master=self.root, data=encoded_img.tobytes())
                        self.label.config(image=tk_img)
                        self.label.image = tk_img 
            except Exception as e:
                print(f"Ошибка при обработке кадра: {e}")

        self.root.after(20, self.check_queue)
    
    def _process_render_task(self, task):
        QUEUE_ID, IMG_ID, WINDOW_NAME = task
        if self.title != WINDOW_NAME:
            self.title = WINDOW_NAME
            self.root.title(self.title)
        img = GlobalVideoMemory.get(queue_id=QUEUE_ID, img_id=IMG_ID)
        if img is not None and self.root.winfo_exists():
            try:
                if len(img.shape) == 3 and img.shape[2] == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                success, encoded_image = cv2.imencode('.ppm', img)
                if success:
                    tk_img = tk.PhotoImage(master = self.root, data=encoded_image.tobytes())
                    self.label.config(image=tk_img)
                    self.label.image = tk_img 
                    self.root.update_idletasks()
                    self.root.update()
            except Exception as e:
                print(f"Ошибка отрисовки кадра: {e}")
    
    def schedule(self, event_input_name, event_input_value, QI, QUEUE_ID, IMG_ID):
        if event_input_name == 'REQ':
            self.frame_queue.put((QUEUE_ID, IMG_ID, self.title))
            return event_input_value, True, "Image queued successfully.", IMG_ID
        return event_input_value, False, "Invalid event input name.", None

    def __del__(self):
        pass
    