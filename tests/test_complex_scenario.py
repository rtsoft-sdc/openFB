"""
Пример комплексного сценария с большим количеством функциональных блоков

Этот пример демонстрирует, как использовать множество блоков вместе для 
реализации сложной автоматизированной системы (например, система управления 
стиральной машиной с фазами цикла).
"""
import pytest
import time
from openfb.resources.function_blocks.events.E_R_TRIG import E_R_TRIG
from openfb.resources.function_blocks.events.E_F_TRIG import E_F_TRIG
from openfb.resources.function_blocks.events.E_CTU import E_CTU
from openfb.resources.function_blocks.events.E_RS import E_RS
from openfb.resources.function_blocks.events.E_T_FF import E_T_FF
from openfb.resources.function_blocks.events.E_DEMUX_4 import E_DEMUX_4
from openfb.resources.function_blocks.events.E_MERGE import E_MERGE
from openfb.resources.function_blocks.events.timers.E_TON import E_TON
from openfb.resources.function_blocks.events.timers.E_TOF import E_TOF
from openfb.resources.function_blocks.events.timers.E_TP import E_TP


class WashingMachineController:
    """
    Контроллер стиральной машины, демонстрирующий использование множества блоков.
    
    Система включает:
    - Детектор начала цикла (rising edge)
    - Счетчик фаз цикла
    - Таймер фаз
    - Мультиплексирование между фазами
    - Контроль состояния (on/off)
    """
    
    # Фазы стирки
    PHASE_IDLE = 0
    PHASE_FILL = 1
    PHASE_WASH = 2
    PHASE_RINSE = 3
    PHASE_SPIN = 4
    PHASE_COMPLETE = 5
    
    def __init__(self):
        # Детектор для начала цикла
        self.start_trigger = E_R_TRIG()
        self.stop_trigger = E_F_TRIG()
        
        # Счетчик фаз
        self.phase_counter = E_CTU()
        
        # Управление состоянием машины (включена/выключена)
        self.power_control = E_RS()
        
        # Таймер для каждой фазы
        self.phase_timers = {
            self.PHASE_FILL: E_TON(),    # Заполнение 30 сек
            self.PHASE_WASH: E_TON(),    # Стирка 120 сек
            self.PHASE_RINSE: E_TON(),   # Полоскание 60 сек
            self.PHASE_SPIN: E_TP(),     # Отжим 45 сек
        }
        
        # Фазовый коммутатор
        self.phase_demux = E_DEMUX_4()
        
        # События объединения
        self.event_merger = E_MERGE()
        
        # Переключатель фаз
        self.phase_toggle = E_T_FF()
        
        # Состояние
        self.is_running = False
        self.current_phase = self.PHASE_IDLE
        self.cycle_count = 0
    
    def start_cycle(self, start_signal: bool):
        """Начать цикл стирки"""
        # Детектор нарастающего фронта для начала
        result = self.start_trigger.schedule('EI', 'START_EVENT', start_signal)
        
        if result:  # Обнаружен нарастающий фронт
            # Включить питание
            power_result = self.power_control.schedule('S', 'POWER_ON')
            self.is_running = True
            self.current_phase = self.PHASE_FILL
            self.cycle_count += 1
            print(f"[CYCLE {self.cycle_count}] Начало цикла стирки")
            return True
        
        return False
    
    def stop_cycle(self, stop_signal: bool):
        """Остановить цикл стирки"""
        # Детектор падающего фронта для остановки
        result = self.stop_trigger.schedule('EI', 'STOP_EVENT', stop_signal)
        
        if result:  # Обнаружен падающий фронт
            # Выключить питание
            self.power_control.schedule('R', 'POWER_OFF')
            self.is_running = False
            self.current_phase = self.PHASE_IDLE
            print(f"[CYCLE {self.cycle_count}] Цикл остановлен")
            return True
        
        return False
    
    def advance_phase(self):
        """Перейти к следующей фазе"""
        if not self.is_running or self.current_phase >= self.PHASE_SPIN:
            return False
        
        # Увеличить счетчик фаз
        counter_result = self.phase_counter.schedule('CU', 'PHASE_UP', 5)
        
        if counter_result and counter_result[2] > self.current_phase:  # CV > current
            self.current_phase += 1
            print(f"[CYCLE {self.cycle_count}] Фаза {self.current_phase}")
            return True
        
        return False
    
    def execute_phase(self, phase: int, duration: float):
        """Выполнить текущую фазу с таймером"""
        if phase not in self.phase_timers:
            return False
        
        timer = self.phase_timers[phase]
        
        # Запустить таймер для фазы
        timer_result = timer.schedule('REQ', 'PHASE_TIMER', True, duration)
        
        if timer_result:
            print(f"[CYCLE {self.cycle_count}] Фаза {phase} выполняется ({duration}s)")
            return True
        
        return False
    
    def check_phase_complete(self, phase: int) -> bool:
        """Проверить завершение текущей фазы"""
        if phase not in self.phase_timers:
            return False
        
        timer = self.phase_timers[phase]
        return timer.Q == True
    
    def simulate_full_cycle(self):
        """Симуляция полного цикла стирки"""
        print("\n" + "="*60)
        print("СИМУЛЯЦИЯ ПОЛНОГО ЦИКЛА СТИРКИ")
        print("="*60)
        
        # Начать цикл
        self.start_cycle(True)
        time.sleep(0.1)
        
        # Фаза заполнения
        print("\nФаза 1: ЗАПОЛНЕНИЕ (30 сек)")
        self.execute_phase(self.PHASE_FILL, 0.3)  # Сокращенно для теста
        time.sleep(0.35)
        
        # Фаза стирки
        print("\nФаза 2: СТИРКА (120 сек)")
        self.advance_phase()
        self.execute_phase(self.PHASE_WASH, 0.5)
        time.sleep(0.55)
        
        # Фаза полоскания
        print("\nФаза 3: ПОЛОСКАНИЕ (60 сек)")
        self.advance_phase()
        self.execute_phase(self.PHASE_RINSE, 0.3)
        time.sleep(0.35)
        
        # Фаза отжима
        print("\nФаза 4: ОТЖИМ (45 сек)")
        self.advance_phase()
        self.execute_phase(self.PHASE_SPIN, 0.4)
        time.sleep(0.45)
        
        # Завершение
        print("\nЦикл ЗАВЕРШЕН")
        self.stop_cycle(False)
        
        print("\n" + "="*60)
        print("СТАТИСТИКА:")
        print(f"  Цикл: {self.cycle_count}")
        print(f"  Фаза: {self.current_phase}")
        print(f"  Статус: {'Работает' if self.is_running else 'Остановлена'}")
        print("="*60)


# ===========================
# ТЕСТЫ КОМПЛЕКСНОГО СЦЕНАРИЯ
# ===========================

class TestWashingMachineIntegration:
    """Интеграционные тесты для контроллера стиральной машины"""
    
    @pytest.mark.integration
    def test_washing_machine_start_stop(self):
        """Тест запуска и остановки стиральной машины"""
        controller = WashingMachineController()
        
        # Начать цикл
        assert controller.start_cycle(True) == True
        assert controller.is_running == True
        assert controller.current_phase == WashingMachineController.PHASE_FILL
        
        # Остановить цикл
        assert controller.stop_cycle(False) == True
        assert controller.is_running == False
        assert controller.current_phase == WashingMachineController.PHASE_IDLE
    
    @pytest.mark.integration
    def test_washing_machine_phase_progression(self):
        """Тест прогрессии фаз"""
        controller = WashingMachineController()
        
        # Начать цикл
        controller.start_cycle(True)
        
        # Проверить начальную фазу
        assert controller.current_phase == WashingMachineController.PHASE_FILL
        
        # Перейти в следующую фазу
        for _ in range(4):
            controller.advance_phase()
            assert controller.current_phase > WashingMachineController.PHASE_FILL
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_washing_machine_full_cycle(self):
        """Тест полного цикла стирки"""
        controller = WashingMachineController()
        controller.simulate_full_cycle()
        
        # Проверить финальное состояние
        assert controller.is_running == False
        assert controller.current_phase == WashingMachineController.PHASE_IDLE
        assert controller.cycle_count == 1


class TestMultipleBlocksInteraction:
    """Тесты взаимодействия множества блоков"""
    
    @pytest.mark.integration
    def test_edge_triggers_with_counter(self):
        """Тест детекторов фронтов со счетчиком"""
        trigger = E_R_TRIG()
        counter = E_CTU()
        
        # Генерировать несколько фронтов
        for i in range(5):
            result = trigger.schedule('EI', f'EVENT_{i}', True)
            if result:
                counter.schedule('CU', result, 10)
    
    @pytest.mark.integration
    def test_timer_state_machine(self):
        """Тест конечного автомата на основе таймеров"""
        # Состояния
        timer_on = E_TON()
        timer_off = E_TOF()
        state_toggle = E_T_FF()
        
        # Включить
        timer_on.schedule('REQ', 'ON', True, 0.1)
        
        # Переключить состояние
        state_toggle.schedule('CLK', 'TOGGLE')
        
        # Выключить
        timer_off.schedule('REQ', 'OFF', False, 0.1)
    
    @pytest.mark.integration
    def test_demux_with_multiple_consumers(self):
        """Тест демультиплексера с несколькими потребителями"""
        demux = E_DEMUX_4()
        consumers = [E_CTU() for _ in range(4)]
        
        # Маршрутизировать события
        for k in range(4):
            result = demux.schedule('EI', 'DEMUX_EVENT', k)
            assert result is not None
            
            # Отправить каждому потребителю его событие
            for i, consumer in enumerate(consumers):
                if result[i]:
                    consumer.schedule('CU', result[i], 10)


if __name__ == '__main__':
    # Запуск симуляции прямо из скрипта
    controller = WashingMachineController()
    controller.simulate_full_cycle()
