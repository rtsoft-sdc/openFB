from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
import numpy as np
import cv2

class FROTHIMAGEGEN:
    def __init__(self):
        self.QUEUE_ID = "def_fl_queue"
        self.imgIDcounter = 0
        self.offset_y = 0
    
    def generate_foam_layer(self, width, height, avg_radius):
        foam = np.zeros((height, width), dtype=np.float32)
        
        num_bubbles = int((width * height) / (np.pi * (avg_radius ** 2)) * 1.5)
        num_bubbles = max(10, min(num_bubbles, 2000))

        cx = np.random.randint(0, width, size=num_bubbles)
        cy = np.random.randint(0, height, size=num_bubbles)
        
        radii = np.random.normal(avg_radius, avg_radius * 0.3, size=num_bubbles)
        radii = np.clip(radii, 2, avg_radius * 2).astype(np.int32)
        
        y_grid, x_grid = np.ogrid[:height, :width]
        
        dist_map = np.ones((height, width), dtype=np.float32) * 1e6
        
        for i in range(num_bubbles):
            r = radii[i]
            x_min, x_max = max(0, cx[i] - r*2), min(width, cx[i] + r*2)
            y_min, y_max = max(0, cy[i] - r*2), min(height, cy[i] + r*2)
            
            d = np.sqrt((x_grid[:, x_min:x_max] - cx[i])**2 + (y_grid[y_min:y_max, :] - cy[i])**2) / r
            
            dist_map[y_min:y_max, x_min:x_max] = np.minimum(dist_map[y_min:y_max, x_min:x_max], d)
            
        inside_mask = dist_map < 1.0
        
        foam[inside_mask] = np.sin(dist_map[inside_mask] * np.pi / 2) ** 2

        rim_mask = (dist_map >= 0.85) & (dist_map <= 1.05)
        foam[rim_mask] += 0.4
        
        foam = cv2.GaussianBlur(foam, (3, 3), 0)
        
        noise = np.random.normal(0, 0.05, foam.shape).astype(np.float32)
        foam = np.clip(foam + noise, 0.0, 1.0)
        
        return (foam * 255).astype(np.uint8)

    def schedule(self, event_input_name, event_input_value, QI, WIDTH, HEIGHT, AVGRADIUS, QUEUE_ID):
        if event_input_name == "INIT":
            if not QI:
                return event_input_value, None, False, None, "DISABLED"
            try:
                GlobalVideoMemory.clear_queue(self.QUEUE_ID)
            except:
                pass
            self.QUEUE_ID = GlobalVideoMemory.get_queue_id(QUEUE_ID)
            return event_input_value, None, True, None, "QUEUE_ID set"
        
        if event_input_name == "REQ":
            if not QI:
                return None, event_input_value, False, None, "DISABLED"
            if AVGRADIUS < 5: 
                AVGRADIUS = 5 

            w = int(WIDTH) if (WIDTH and WIDTH > 0) else 800
            h = int(HEIGHT) if (HEIGHT and HEIGHT > 0) else 600
            r = int(AVGRADIUS) if (AVGRADIUS and AVGRADIUS >= 5) else 15
            
            foam_frame = self.generate_foam_layer(w, h, r)
            animated_frame = foam_frame[self.offset_y:self.offset_y+HEIGHT, 0:WIDTH]
            current_id = self.imgIDcounter
            GlobalVideoMemory.set(queue_id=self.QUEUE_ID, img_id=current_id, frame=animated_frame)
            self.imgIDcounter+=1
            return None, event_input_value, True, current_id, "Frame created"