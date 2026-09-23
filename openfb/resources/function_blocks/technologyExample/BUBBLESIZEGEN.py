from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
import numpy as np
import math

class BUBBLESIZEGEN:
    
    def get_bubble_size_by_level(H_p):
        """
        Расчет среднего размера пузырька (мм) только на основе уровня пульпы (м).
        Внутренние коэффициенты зафиксированы под стандартную медно-никелевую ячейку.
        """
        # 1. Задаем базовые константы оборудования и процесса
        H_tot = 4.5       # Номинальная высота флотомашины (м)
        d_min = 1.2       # Минимальный базовый размер пузырька при максимальном уровне пульпы (мм)
        k_coalesce = 3.3  # Интегральный коэффициент укрупнения пены для сульфидной руды
        
        # Ограничение: уровень пульпы не может превышать край флотомашины
        if H_p >= H_tot:
            return d_min
            
        # 2. Вычисляем высоту пены: чем выше пульпа, тем меньше пена
        H_f = H_tot - H_p
        
        # 3. Эмпирическая экспоненциальная зависимость
        d_b = d_min * math.exp(k_coalesce * H_f)
        
        return round(d_b, 2)
    
    def schedule(self, event_input_name, event_input_value, LEVEL):

        if event_input_name == "REQ":
            bubblesize = None
            if LEVEL:
                bubblesize = self.get_bubble_size_by_level(LEVEL)
            return event_input_value, bubblesize