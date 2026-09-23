import tkinter as tk
import threading
import logging


class SLIDER:
    def __init__(self, title="BUBBLESIZE Slider"):
        self.title = title
        self.window_is_open = False
        self.root = None
        self.slider = None
        self.current_value = 40
        self.min_val = 10
        self.max_val = 200

        self.run_display_thread = threading.Thread(target=self.init_window, daemon=True)
        self.run_display_thread.start()
        
    def init_window(self):
        try:
            self.root = tk.Tk()
            self.root.title(self.title)
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            self.root.geometry("200x350")
            
            label = tk.Label(self.root, text="Value:", font=("Courier", 14))
            label.pack(pady=(10, 0))
            
            self.slider = tk.Scale(
                self.root, 
                from_=self.max_val, 
                to=self.min_val, 
                orient=tk.VERTICAL, 
                length=220, 
                tickinterval=50, 
                showvalue=True, 
                command=self._on_slider
            )
            self.slider.set(self.current_value)
            self.slider.pack(expand=True, fill=tk.Y, pady=10)
            
            self.window_is_open = True
            self.root.withdraw()

            self.root.mainloop()
        except Exception as e:
            logging.error(f"Error Tkinter: {e}")
            
    def _on_slider(self, value):
        try:
            self.current_value = int(value)
        except Exception as e:
            logging.error(f"Err reading slider: {e}")

    def set_limits(self, min_val, max_val):
        if self.root and self.window_is_open:
            self.root.after(0, lambda: self._apply_limits(min_val, max_val))

    def _apply_limits(self, min_val, max_val):
        try:
            self.min_val = min_val
            self.max_val = max_val
            
            tick = max(1, abs(max_val - min_val) // 5)
            
            self.slider.config(
                from_=max_val,
                to=min_val,
                tickinterval=tick
            )
            
            self.current_value = min_val
            self.slider.set(self.current_value)
            
            self.root.deiconify()
        except Exception as e:
            logging.error(f"Error applying limits: {e}")

    def schedule(self, event_input_name, event_input_value, MINV, MAXV):
        if event_input_name == "INIT":
            self.set_limits(min_val=MINV, max_val=MAXV)
            return event_input_value, None, None
            
        if event_input_name == "REQ":
            if self.window_is_open:
                return None, event_input_value, self.current_value
            return None, event_input_value, None

    def on_close(self):
        self.window_is_open = False
        if self.root is not None:
            self.root.quit()
            self.root.destroy()