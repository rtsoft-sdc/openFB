from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
import numpy as np
import cv2
import time
import json
from collections import deque

class MULTIPLOTTER:
    def __init__(self):
        self.imgIDcounter = 2
        self.QUEUE_ID = "def_multiplot_queue"
        self.offset_y = 0
        self.is_initialized = False
        
    def plot_init(self, width: int = 1000, height: int = 600, max_plots: int = 8):
        self.width = width
        self.height = height
        self.max_plots = min(max_plots, 8)
        self.buffers = [deque() for _ in range(self.max_plots)]

        self.plot_configs = {
            i: {
                "min_val": 0.0,
                "max_val": 100.0,
                "color": self._get_default_color(i),
                "label": f"Param {i+1}",
                "offset": 0.0 
            }
            for i in range(self.max_plots)
        }

        self.bg_color = (20, 20, 20)
        self.axis_color = (200, 200, 200)
        self.text_color = (255, 255, 255)
        self.y_axis_label = "Values"
        self.time_window = 5 * 60

        self.padding_top = 50
        self.padding_bottom = 80
        self.padding_left = 80
        self.padding_right = 40
        
        self.is_initialized = True

    def _get_default_color(self, idx: int) -> tuple:
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), 
            (255, 0, 255), (255, 255, 0), (0, 165, 255), (0, 252, 124)
        ]
        return colors[idx % len(colors)]

    def set_background_color(self, color: tuple):
        self.bg_color = color

    def set_y_axis_label(self, label: str):
        self.y_axis_label = label

    def configure_plot(self, idx: int, min_val: float, max_val: float, label: str, color: tuple = None):
        if 0 <= idx < self.max_plots:
            self.plot_configs[idx]["min_val"] = float(min_val)
            self.plot_configs[idx]["max_val"] = float(max_val)
            self.plot_configs[idx]["label"] = label
            if color is not None:
                self.plot_configs[idx]["color"] = color

    def _parse_and_apply_params(self, idx: int, params_input):
        """
        format: '{"min": 0, "max": 100, "offset": 50, "color": [255, 0, 0], "label": "MyParam"}'
        """
        if not params_input:
            return

        if isinstance(params_input, str):
            try:
                data = json.loads(params_input)
            except (json.JSONDecodeError, TypeError):
                return
        elif isinstance(params_input, dict):
            data = params_input
        else:
            return

        config = self.plot_configs[idx]

        min_val = data.get("min", data.get("min_val", config["min_val"]))
        max_val = data.get("max", data.get("max_val", config["max_val"]))
        label = data.get("label", config["label"])
        offset = data.get("offset", config["offset"])
        
        color = config["color"]
        raw_color = data.get("color")
        if isinstance(raw_color, (list, tuple)) and len(raw_color) == 3:
            color = (int(raw_color[0]), int(raw_color[1]), int(raw_color[2]))
        elif isinstance(raw_color, str):
            c_parts = raw_color.split(',')
            if len(c_parts) == 3:
                color = (int(c_parts[0]), int(c_parts[1]), int(c_parts[2]))

        try:
            self.configure_plot(idx, float(min_val), float(max_val), str(label), color)
            self.plot_configs[idx]["offset"] = float(offset)
        except (ValueError, TypeError):
            pass

    def add_value(self, idx: int, value: float):
        if 0 <= idx < self.max_plots:
            current_time = time.time()
            self.buffers[idx].append((current_time, float(value)))
            self._clear_old_data(idx, current_time)

    def _clear_old_data(self, idx: int, current_time: float):
        while self.buffers[idx] and (current_time - self.buffers[idx][0][0]) > self.time_window:
            self.buffers[idx].popleft()

    def plot(self) -> np.ndarray:
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        img[:] = self.bg_color

        current_time = time.time()
        start_time = current_time - self.time_window

        graph_x_min = self.padding_left
        graph_x_max = self.width - self.padding_right
        graph_y_min = self.padding_top
        graph_y_max = self.height - self.padding_bottom

        for i in range(self.max_plots):
            self._clear_old_data(i, current_time)

        cv2.line(img, (graph_x_min, graph_y_max), (graph_x_max, graph_y_max), self.axis_color, 2)
        cv2.line(img, (graph_x_min, graph_y_min), (graph_x_min, graph_y_max), self.axis_color, 2)

        cv2.putText(img, self.y_axis_label, (graph_x_min + 10, graph_y_min - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 1, cv2.LINE_AA)

        for min_offset in range(0, 6, 1):
            x_pos = graph_x_max - int((min_offset * 60) / self.time_window * (graph_x_max - graph_x_min))
            cv2.line(img, (x_pos, graph_y_max), (x_pos, graph_y_max + 5), self.axis_color, 1)
            text = f"-{min_offset}m" if min_offset > 0 else "Now"
            cv2.putText(img, text, (x_pos - 15, graph_y_max + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.text_color, 1, cv2.LINE_AA)

        for i in range(self.max_plots):
            points = self.buffers[i]
            if len(points) < 2:
                continue

            config = self.plot_configs[i]
            min_val = config["min_val"]
            max_val = config["max_val"]
            color = config["color"]
            val_range = max_val - min_val if max_val != min_val else 1.0

            prev_pixel = None
            for t, val in points:
                val = max(min(val, max_val), min_val)
                x_ratio = (t - start_time) / self.time_window
                x_pixel = graph_x_min + int(x_ratio * (graph_x_max - graph_x_min))

                y_ratio = (val - min_val) / val_range
                y_pixel = graph_y_max - int(y_ratio * (graph_y_max - graph_y_min))
                current_pixel = (x_pixel, y_pixel)

                if prev_pixel is not None:
                    cv2.line(img, prev_pixel, current_pixel, color, 2, cv2.LINE_AA)
                prev_pixel = current_pixel

        legend_x = graph_x_min
        legend_y = graph_y_max + 50
        spacing_x = 115 

        for i in range(self.max_plots):
            config = self.plot_configs[i]
            if legend_x + 100 > graph_x_max:
                legend_x = graph_x_min
                legend_y += 20

            cv2.rectangle(img, (legend_x, legend_y - 10), (legend_x + 15, legend_y), config["color"], -1)
            cv2.putText(img, f"{config['label']}", (legend_x + 22, legend_y - 1), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.text_color, 1, cv2.LINE_AA)
            legend_x += spacing_x

        return img

    def schedule(self, event_input_name, event_input_value, QI, DST_QUEUE_ID, V1, PARAMS1, V2, PARAMS2, V3, PARAMS3, V4, PARAMS4, V5, PARAMS5, V6, PARAMS6, V7, PARAMS7, V8, PARAMS8):
        
        if event_input_name == "INIT":
            try:
                GlobalVideoMemory.clear_queue(self.QUEUE_ID)
            except:
                pass
            
            if DST_QUEUE_ID:
                self.QUEUE_ID = GlobalVideoMemory.get_queue_id(DST_QUEUE_ID)
                
            if not self.is_initialized:
                self.plot_init()
                
            return event_input_value, None, True, None, "QUEUE_ID set"
        
        if event_input_name == "REQ":
            if not QI:
                return None, event_input_value, False, None, "DISABLED"
            
            if not self.is_initialized:
                self.plot_init()

            values = [V1, V2, V3, V4, V5, V6, V7, V8]
            params_list = [PARAMS1, PARAMS2, PARAMS3, PARAMS4, PARAMS5, PARAMS6, PARAMS7, PARAMS8]

            for i in range(self.max_plots):
                if values[i] is not None:
                    self._parse_and_apply_params(i, params_list[i])
                    
                    try:
                        raw_val = float(values[i])
                        offset = self.plot_configs[i].get("offset", 0.0)
                        shifted_val = raw_val + offset
                        
                        self.add_value(i, shifted_val)
                    except (ValueError, TypeError):
                        pass

            try:
                frame = self.plot()                
                self.imgIDcounter += 1
                GlobalVideoMemory.set(queue_id=self.QUEUE_ID, img_id=self.imgIDcounter, frame=frame)
                return None, event_input_value, True, self.imgIDcounter, "OK"
            except Exception as e:
                return None, event_input_value, False, None, f"RENDER_ERR: {str(e)}"