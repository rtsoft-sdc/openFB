from openfb.resources.function_blocks.openCV.globalVideoMemory import GlobalVideoMemory
import numpy as np
import cv2

class RECOGNIZER:
    def __init__(self):
        self.imgIDcounter = 0
        self.QUEUE_ID = "default_req_queue"
        pass
        
    def analyze_foam_frst_master(self, image_gray, avg_diameter):
        """
        Высокоточный алгоритм на основе Fast Radial Symmetry Transform (FRST).
        Находит мелкие, средние, крупные и плотно сжатые пузырьки.
        Полностью невосприимчив к шуму на широких светлых ободках.
        """
        output_frame = cv2.cvtColor(image_gray, cv2.COLOR_GRAY2BGR)
        h, w = image_gray.shape
        
        # 1. ДЕЛИКАТНОЕ СГЛАЖИВАНИЕ ШУМА
        # Сглаживаем только микро-шум плёнок, сохраняя глобальные склоны куполов
        blurred = cv2.GaussianBlur(image_gray, (5, 5), 0)
        
        # 2. ВЫЧИСЛЕНИЕ ВЕКТОРОВ НАПРАВЛЕНИЙ (ГРАДИЕНТЫ СОБЕЛЛЯ)
        grad_x = cv2.Sobel(blurred, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(blurred, cv2.CV_32F, 0, 1, ksize=3)
        grad_mag = cv2.magnitude(grad_x, grad_y)
        
        # Нормализуем градиенты (избегаем деления на ноль)
        grad_mag[grad_mag == 0] = 1e-5
        unit_x = grad_x / grad_mag
        unit_y = grad_y / grad_mag
        
        # 3. МАТРИЦА РАДИАЛЬНОГО НАКОПЛЕНИЯ (Голосование за центры)
        # Создаем холст, куда лучи градиентов будут "голосовать" за предполагаемые центры пузырей
        S = np.zeros((h, w), dtype=np.float32)
        
        # Задаем диапазон радиусов для голосования (от мелких до крупных пузырей)
        min_r = max(3, int(avg_diameter * 0.25))
        max_r = min(int(h/2), int(avg_diameter * 1.3))
        radii_to_check = range(min_r, max_r, max(1, int(avg_diameter * 0.15)))
        
        for r in radii_to_check:
            # Смещение по направлению градиента наружу (к темным границам) 
            # и внутрь (к центрам куполов)
            for sign in [-1, 1]:
                shift_x = np.round(sign * unit_x * r).astype(np.int32)
                shift_y = np.round(sign * unit_y * r).astype(np.int32)
                
                # Координатная сетка со смещением
                y_indices, x_indices = np.indices((h, w))
                nx = np.clip(x_indices + shift_x, 0, w - 1)
                ny = np.clip(y_indices + shift_y, 0, h - 1)
                
                # Накапливаем голоса. Центры пузырей получат максимальные пики
                S[ny, nx] += grad_mag
                
        # Размываем матрицу голосования, чтобы слить близкие пики в один мощный центр
        S_blur_k = int(avg_diameter * 0.3) | 1
        S_blur_k = max(5, S_blur_k)
        S_smooth = cv2.GaussianBlur(S, (S_blur_k, S_blur_k), 0)
        
        # 4. ПОИСК ЛОКАЛЬНЫХ МАКСИМУМОВ НА КАРТЕ СИММЕТРИИ (Local NMS)
        # Окно поиска центра пропорционально размеру пузырей
        window_size = int(avg_diameter * 0.5) | 1
        window_size = max(5, window_size)
        kernel_nms = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (window_size, window_size))
        
        local_max_S = cv2.dilate(S_smooth, kernel_nms)
        peaks_mask = (S_smooth == local_max_S) & (S_smooth > np.mean(S_smooth) * 1.5)
        y_peaks, x_peaks = np.where(peaks_mask)
        
        # Пул кандидатов
        candidates = []
        
        # 5. ИНДИВИДУАЛЬНЫЙ ЗАМЕР РАДИУСА ИЗ КАЖДОГО ЦЕНТРА (Лучевой метод 3.0)
        for cy, cx in zip(y_peaks, x_peaks):
            # Исключаем края кадра
            margin = max(4, int(avg_diameter * 0.15))
            if cx < margin or cx > w - margin or cy < margin or cy > h - margin:
                continue
                
            # Пускаем 8 лучей из найденного центра, чтобы найти внешнюю кромку ободка (пик градиента)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            r_samples = []
            max_search_r = int(avg_diameter * 1.8)
            
            for dx, dy in directions:
                detected_r = max_search_r
                best_grad = 0
                best_r = 0
                
                len_step = np.sqrt(dx**2 + dy**2)
                step_x, step_y = dx / len_step, dy / len_step
                
                for r_step in range(2, max_search_r):
                    nx = int(cx + step_x * r_step)
                    ny = int(cy + step_y * r_step)
                    
                    if nx < 0 or nx >= w or ny < 0 or ny >= h:
                        break
                        
                    # Ищем точку максимального изменения контраста (внешний край светлого ободка)
                    current_grad = grad_mag[ny, nx]
                    if current_grad > best_grad:
                        best_grad = current_grad
                        best_r = r_step
                        
                    # Дополнительный триггер: резкий темный стык пены (вода)
                    if blurred[ny, nx] < 40:
                        detected_r = r_step
                        break
                        
                if detected_r == max_search_r and best_r > 0:
                    detected_r = best_r
                    
                r_samples.append(detected_r)
                
            # Медиана защищает от "промахов" лучей сквозь слипшиеся стенки соседей
            bubble_radius = np.median(r_samples)
            bubble_diameter = bubble_radius * 2.0
            
            # Фильтр экстремальных размеров
            if bubble_diameter < 6 or bubble_diameter > (avg_diameter * 2.3):
                continue
                
            candidates.append({'cx': int(cx), 'cy': int(cy), 'r': bubble_radius, 'd': bubble_diameter})

        # 6. YOLO-STYLE ФИЛЬТРАЦИЯ НАЛОЖЕНИЙ (Очистка ложных дубликатов центров)
        candidates.sort(key=lambda x: x['d'], reverse=True)
        final_bubbles = []
        
        for child in candidates:
            is_fraud = False
            for parent in final_bubbles:
                dist = np.sqrt((child['cx'] - parent['cx'])**2 + (child['cy'] - parent['cy'])**2)
                
                # Если центр мелкого пузыря лежит внутри геометрии крупного — это ложный приграничный шум
                if dist < parent['r'] * 0.95 and child['d'] < parent['d'] * 0.65:
                    is_fraud = True
                    break
                    
                # Если два центра слишком близко сидят друг к другу (раздвоение пика)
                if dist < (parent['r'] + child['r']) * 0.35:
                    is_fraud = True
                    break
                    
            if not is_fraud:
                final_bubbles.append(child)

        # 7. МЕТРОЛОГИЯ И ОТРИСОВКА
        diameters = []
        for b in final_bubbles:
            # Исключаем урезанные рамкой пузыри из статистики
            if b['cx'] - b['r'] < 2 or b['cx'] + b['r'] > w - 2 or \
            b['cy'] - b['r'] < 2 or b['cy'] + b['r'] > h - 2:
                continue
                
            diameters.append(b['d'])
            
            # Крупные пузыри — ЛАЗУРНЫЙ контур, мелкие и средние — ЗЕЛЕНЫЙ
            color = (255, 180, 0) if b['d'] > avg_diameter else (0, 255, 0)
            cv2.circle(output_frame, (b['cx'], b['cy']), int(b['r']), color, 1)
            cv2.circle(output_frame, (b['cx'], b['cy']), 2, (0, 255, 255), -1)
            
        if not diameters:
            return output_frame, 0.0, 0.0, 0.0
            
        return output_frame, float(np.min(diameters)), float(np.max(diameters)), float(np.mean(diameters))


    def estimate_avg_diameter_fft(self, image_gray):
        """
        Автоматически оценивает средний диаметр пузырьков с помощью преобразования Фурье.
        """
        # Вычисляем дискретное преобразование Фурье
        f = np.fft.fft2(image_gray)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
        
        # Находим центр спектра
        cy, cx = magnitude_spectrum.shape[0] // 2, magnitude_spectrum.shape[1] // 2
        
        # Строим радиальный профиль частот от центра наружу
        y, x = np.indices(magnitude_spectrum.shape)
        r = np.sqrt((x - cx)**2 + (y - cy)**2).astype(int)
        
        # Суммируем интенсивность частот на каждом радиусе
        radial_profile = np.bincount(r.ravel(), weights=magnitude_spectrum.ravel())
        
        # Пропускаем самую низкую частоту (центр/постоянную составляющую)
        # Ищем первый выраженный пик, который отвечает за структуру пены
        min_look_r = 5
        if len(radial_profile) > min_look_r:
            peak_freq_r = np.argmax(radial_profile[min_look_r:]) + min_look_r
            if peak_freq_r > 0:
                # Диаметр обратно пропорционален частоте пространственного спектра
                estimated_dia = max(image_gray.shape[0], image_gray.shape[1]) / peak_freq_r
                return np.clip(estimated_dia, 15, 120) # Ограничиваем разумный диапазон
                
        return 40.0 # Дефолтное значение, если спектр чистый



    def schedule(self, event_input_name, event_input_value, SRC_QUEUE_ID, IMG_ID, DST_QUEUE_ID):

        if event_input_name == "REQ":
            src_queue_id = GlobalVideoMemory.get_queue_id(SRC_QUEUE_ID)
            dstqueue = GlobalVideoMemory.get_queue_id(DST_QUEUE_ID)
            img = GlobalVideoMemory.get(src_queue_id, IMG_ID)
            if img is not None:
                avg_diameter = self.estimate_avg_diameter_fft(img)
                print(f"\n{avg_diameter}")
                visualized_frame, min_d, max_d, avg_d = self.analyze_foam_frst_master(img, avg_diameter)
                self.imgIDcounter+=1

                GlobalVideoMemory.set(queue_id=dstqueue, img_id=self.imgIDcounter, frame=visualized_frame)
                return event_input_value, self.imgIDcounter, avg_d, min_d, max_d, "Frame processed"
            return event_input_value, None, None, None, None, "Error while processing"