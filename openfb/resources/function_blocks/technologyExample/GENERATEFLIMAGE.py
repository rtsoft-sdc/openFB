from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
import numpy as np
import cv2

class GENERATEFLIMAGE:
    def __init__(self):
        self.QUEUE_ID = "def_fl_queue"
        self.imgIDcounter = 0
        self.offset_y = 0
    
    def generate_foam_layer(self, width, height, avg_radius):
        """
        Генерирует фотореалистичную текстуру пены (вид сверху).
        """
        # Создаем базовый фон (темная основа жидких границ)
        foam = np.zeros((height, width), dtype=np.float32)
        
        # Задаем параметры распределения пузырьков
        # Количество пузырьков зависит от их радиуса, чтобы заполнить экран
        num_bubbles = int((width * height) / (np.pi * (avg_radius ** 2)) * 1.5)
        num_bubbles = max(10, min(num_bubbles, 2000)) # Ограничиваем лимиты
        
        # Случайные координаты центров пузырьков

        cx = np.random.randint(0, width, size=num_bubbles)
        cy = np.random.randint(0, height, size=num_bubbles)
        
        # Радиусы с небольшим случайным отклонением от среднего
        radii = np.random.normal(avg_radius, avg_radius * 0.3, size=num_bubbles)
        radii = np.clip(radii, 2, avg_radius * 2).astype(np.int32)
        
        # Сетка координат для быстрого вычисления расстояний
        y_grid, x_grid = np.ogrid[:height, :width]
        
        # Вычисляем карту минимальных расстояний до центров сфер
        # Это создаст структуру ячеек Вороного со сглаженными переходами
        dist_map = np.ones((height, width), dtype=np.float32) * 1e6
        
        for i in range(num_bubbles):
            # Ограничиваем область просчета локальным квадратом вокруг пузырька для ускорения
            r = radii[i]
            x_min, x_max = max(0, cx[i] - r*2), min(width, cx[i] + r*2)
            y_min, y_max = max(0, cy[i] - r*2), min(height, cy[i] + r*2)
            
            # Расстояние от каждой точки до центра текущего пузырька, нормированное на его радиус
            d = np.sqrt((x_grid[:, x_min:x_max] - cx[i])**2 + (y_grid[y_min:y_max, :] - cy[i])**2) / r
            
            # Записываем минимальное относительное расстояние
            dist_map[y_min:y_max, x_min:x_max] = np.minimum(dist_map[y_min:y_max, x_min:x_max], d)
            
        # Фотореалистичный шейдинг пены:
        # 1. Пузырьки прозрачные, свет преломляется на границах. 
        # Внутренняя часть вогнутая/выпуклая, края дают яркие блики, а стыки — темные.
        
        # Маска самих пузырьков (где расстояние меньше радиуса)
        inside_mask = dist_map < 1.0
        
        # Эффект линзы / 3D сферы (ближе к краям значение стремится к 1)
        # На краях пузырька свет переотражается сильнее (эффект Френеля)
        foam[inside_mask] = np.sin(dist_map[inside_mask] * np.pi / 2) ** 2
        
        # Создаем яркий белый ободок на самой границе пузырька
        rim_mask = (dist_map >= 0.85) & (dist_map <= 1.05)
        foam[rim_mask] += 0.4
        
        # Размытие границ пены и добавление шума для реалистичности водных пленок
        foam = cv2.GaussianBlur(foam, (3, 3), 0)
        
        # Добавляем мягкий фоновый шум (имитация микропузырьков и неоднородностей воды)
        noise = np.random.normal(0, 0.05, foam.shape).astype(np.float32)
        foam = np.clip(foam + noise, 0.0, 1.0)
        
        # Переводим в 8-битный формат градаций серого (0-255)
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

            #SOMETIMES WIDTH HEIGHT 0,0?????
            w = int(WIDTH) if (WIDTH and WIDTH > 0) else 800
            h = int(HEIGHT) if (HEIGHT and HEIGHT > 0) else 600
            r = int(AVGRADIUS) if (AVGRADIUS and AVGRADIUS >= 5) else 15
            
            foam_frame = self.generate_foam_layer(w, h, r)
            animated_frame = foam_frame[self.offset_y:self.offset_y+HEIGHT, 0:WIDTH]
            current_id = self.imgIDcounter
            GlobalVideoMemory.set(queue_id=self.QUEUE_ID, img_id=current_id, frame=animated_frame)
            self.imgIDcounter+=1
            return None, event_input_value, True, current_id, "Frame created"