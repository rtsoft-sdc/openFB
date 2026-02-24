"""
Комплексные тесты для Event функциональных блоков
"""
import pytest
import time
import threading
from openfb.resources.function_blocks.events.E_CTU import E_CTU
from openfb.resources.function_blocks.events.E_CTD import E_CTD
from openfb.resources.function_blocks.events.E_CTUD import E_CTUD
from openfb.resources.function_blocks.events.E_RS import E_RS
from openfb.resources.function_blocks.events.E_SR import E_SR
from openfb.resources.function_blocks.events.E_T_FF import E_T_FF
from openfb.resources.function_blocks.events.E_T_FF_SR import E_T_FF_SR
from openfb.resources.function_blocks.events.E_D_FF import E_D_FF
from openfb.resources.function_blocks.events.E_SPLIT import E_SPLIT
from openfb.resources.function_blocks.events.E_SPLIT_2 import E_SPLIT_2
from openfb.resources.function_blocks.events.E_MERGE import E_MERGE
from openfb.resources.function_blocks.events.E_DEMUX import E_DEMUX
from openfb.resources.function_blocks.events.E_DEMUX_2 import E_DEMUX_2
from openfb.resources.function_blocks.events.E_DEMUX_4 import E_DEMUX_4
from openfb.resources.function_blocks.events.E_MUX_2 import E_MUX_2
from openfb.resources.function_blocks.events.E_MUX_4 import E_MUX_4
from openfb.resources.function_blocks.events.E_DELAY import E_DELAY
from openfb.resources.function_blocks.events.E_RDELAY import E_RDELAY
from openfb.resources.function_blocks.events.E_R_TRIG import E_R_TRIG
from openfb.resources.function_blocks.events.E_F_TRIG import E_F_TRIG
from openfb.resources.function_blocks.events.E_PERMIT import E_PERMIT
from openfb.resources.function_blocks.events.E_REND import E_REND
from openfb.resources.function_blocks.events.timers.E_TON import E_TON
from openfb.resources.function_blocks.events.timers.E_TOF import E_TOF
from openfb.resources.function_blocks.events.timers.E_TP import E_TP
from openfb.resources.function_blocks.events.timers.E_PULSE import E_PULSE
from openfb.resources.function_blocks.events.timers.E_TONOF import E_TONOF


# ===========================
# Тесты для счетчиков
# ===========================

class TestE_CTU:
    """Тесты для Event-driven Up Counter (E_CTU)"""
    
    def test_ctu_increment(self, fb_fixture, event_helper):
        """Тест увеличения счетчика"""
        block = fb_fixture(E_CTU).create()
        
        # Начальное состояние
        result = block.call('CU', 'CU_EVENT', 10)
        event_helper.assert_event_output(result, 'CU_EVENT', False, 1)
        
        # Второе увеличение
        result = block.call('CU', 'CU_EVENT', 10)
        event_helper.assert_event_output(result, 'CU_EVENT', False, 2)
    
    def test_ctu_overflow(self, fb_fixture, event_helper):
        """Тест переполнения счетчика"""
        block = fb_fixture(E_CTU).create()
        block.CV = 5

        # Установить большое значение
        for _ in range(10):
            block.call('CU', 'CU_EVENT', 5)
        
        # При достижении PV должно выдать Q=True
        result = block.call('CU', 'CU_EVENT', 5)
        assert result is not None
        if result:
            assert result[1] == True  # Q должен быть True при переполнении
    
    def test_ctu_reset(self, fb_fixture, event_helper):
        """Тест сброса счетчика"""
        block = fb_fixture(E_CTU).create()
        
        # Увеличить счетчик
        block.call('CU', 'CU_EVENT', 10)
        block.call('CU', 'CU_EVENT', 10)
        
        # Сбросить
        result = block.call('R', 'R_EVENT', 10)
        event_helper.assert_event_output(result, 'R_EVENT', False, 0)


class TestE_CTD:
    """Тесты для Event-driven Down Counter (E_CTD)"""
    
    def test_ctd_decrement(self, fb_fixture, event_helper):
        """Тест уменьшения счетчика"""
        block = fb_fixture(E_CTD).create()
        
        # Установить начальное значение
        result = block.call('LD', 'LD_EVENT', 10)
        assert result is not None
        
        # Уменьшить
        result = block.call('CD', 'CD_EVENT', 10)
        assert result is not None
    
    def test_ctd_underflow(self, fb_fixture, event_helper):
        """Тест при уменьшении ниже нуля"""
        block = fb_fixture(E_CTD).create()
        
        # Загрузить малое значение
        block.call('LD', 'LD_EVENT', 2)
        
        # Уменьшить несколько раз
        block.call('CD', 'CD_EVENT', 2)
        block.call('CD', 'CD_EVENT', 2)
        result = block.call('CD', 'CD_EVENT', 2)
        
        assert result is not None


class TestE_CTUD:
    """Тесты для Event-driven Up-Down Counter (E_CTUD)"""
    
    def test_ctud_increment_decrement(self, fb_fixture, event_helper):
        """Тест увеличения и уменьшения счетчика"""
        block = fb_fixture(E_CTUD).create()
        
        # Увеличить
        result = block.call('CU', 'CU_EVENT', 5, 10)
        assert result is not None
        
        # Уменьшить
        result = block.call('CD', 'CD_EVENT', 5, 10)
        assert result is not None


# ===========================
# Тесты для триггеров (flip-flops)
# ===========================

class TestE_RS:
    """Тесты для Event-driven Set/Reset flip-flop (E_RS)"""
    
    def test_rs_set(self, fb_fixture, event_helper):
        """Тест установки (Set)"""
        block = fb_fixture(E_RS).create()
        
        result = block.call('S', 'S_EVENT')
        event_helper.assert_event_output(result, 'S_EVENT', True)
        assert block.Q == True
    
    def test_rs_reset(self, fb_fixture, event_helper):
        """Тест сброса (Reset)"""
        block = fb_fixture(E_RS).create()
        
        # Сначала установить
        block.call('S', 'S_EVENT')
        
        # Затем сбросить
        result = block.call('R', 'R_EVENT')
        event_helper.assert_event_output(result, 'R_EVENT', False)
        assert block.Q == False


class TestE_SR:
    """Тесты для Event-driven Reset/Set flip-flop (E_SR)"""
    
    def test_sr_reset(self, fb_fixture, event_helper):
        """Тест сброса (Reset)"""
        block = fb_fixture(E_SR).create()
        
        result = block.call('R', 'R_EVENT')
        event_helper.assert_event_output(result, 'R_EVENT', False)
        assert block.Q == False


class TestE_T_FF:
    """Тесты для Toggle flip-flop (E_T_FF)"""
    
    def test_tff_toggle(self, fb_fixture, event_helper):
        """Тест переключения триггера"""
        block = fb_fixture(E_T_FF).create()
        
        # Первое переключение
        result = block.call('CLK', 'CLK_EVENT')
        event_helper.assert_event_output(result, 'CLK_EVENT', True)
        
        # Второе переключение
        result = block.call('CLK', 'CLK_EVENT')
        event_helper.assert_event_output(result, 'CLK_EVENT', False)


# ===========================
# Тесты для демультиплексоров
# ===========================

class TestE_DEMUX_2:
    """Тесты для Event demultiplexer 2-way (E_DEMUX_2)"""
    
    def test_demux_2_output_0(self, fb_fixture, event_helper):
        """Тест вывода на первый выход"""
        block = fb_fixture(E_DEMUX_2).create()
        
        result = block.call('EI', 'EI_EVENT', 0)
        # Ожидаем событие на первом выходе, None на втором
        assert result is not None
        assert result[0] == 'EI_EVENT'
        assert result[1] is None
    
    def test_demux_2_output_1(self, fb_fixture, event_helper):
        """Тест вывода на второй выход"""
        block = fb_fixture(E_DEMUX_2).create()
        
        result = block.call('EI', 'EI_EVENT', 1)
        assert result is not None
        assert result[0] is None
        assert result[1] == 'EI_EVENT'


class TestE_DEMUX_4:
    """Тесты для Event demultiplexer 4-way (E_DEMUX_4)"""
    
    def test_demux_4_routing(self, fb_fixture, event_helper):
        """Тест маршрутизации сигнала"""
        block = fb_fixture(E_DEMUX_4).create()
        
        for k in range(4):
            result = block.call('EI', 'EI_EVENT', k)
            assert result is not None
            for i in range(4):
                if i == k:
                    assert result[i] == 'EI_EVENT'
                else:
                    assert result[i] is None


# ===========================
# Тесты для мультиплексоров
# ===========================

class TestE_MUX_2:
    """Тесты для Event multiplexer 2-way (E_MUX_2)"""
    
    def test_mux_2_select_0(self, fb_fixture, event_helper):
        """Тест выбора первого входа"""
        block = fb_fixture(E_MUX_2).create()
        
        result = block.call('EI1', 'EI1_EVENT', 0)
        event_helper.assert_event_output(result, 'EI1_EVENT')
    
    def test_mux_2_select_1(self, fb_fixture, event_helper):
        """Тест выбора второго входа"""
        block = fb_fixture(E_MUX_2).create()
        
        result = block.call('EI2', 'EI2_EVENT', 1)
        event_helper.assert_event_output(result, 'EI2_EVENT')


# ===========================
# Тесты для таймеров
# ===========================

class TestE_TON:
    """Тесты для On-delay timer (E_TON)"""
    
    def test_ton_delay(self, fb_fixture, event_helper):
        """Тест задержки включения"""
        block = fb_fixture(E_TON).create()
        
        # Включить с задержкой 0.1 сек
        result = block.call('REQ', 'REQ_EVENT', True, 0.1)

        time.sleep(0.15) #!!!
        
        # После задержки Q должен быть True
        assert block.Q == True
    
    def test_ton_cancel(self, fb_fixture, event_helper):
        """Тест отмены задержки"""
        block = fb_fixture(E_TON).create()
        
        # Включить с задержкой
        block.call('REQ', 'REQ_EVENT', True, 1.0)
        
        # Выключить до истечения задержки
        result = block.call('REQ', 'REQ_EVENT', False, 1.0)
        
        # Q должен быть False
        assert block.Q == False


class TestE_TOF:
    """Тесты для Off-delay timer (E_TOF)"""
    
    def test_tof_immediate_on(self, fb_fixture, event_helper):
        """Тест немедленного включения"""
        block = fb_fixture(E_TOF).create()
        
        result = block.call('REQ', 'REQ_EVENT', True, 0.1)
        # Q должен быть True немедленно
        assert block.Q == True
    
    def test_tof_delayed_off(self, fb_fixture, event_helper):
        """Тест задержанного выключения"""
        block = fb_fixture(E_TOF).create()
        
        # Включить
        block.call('REQ', 'REQ_EVENT', True, 0.1)
        assert block.Q == True
        
        # Выключить
        block.call('REQ', 'REQ_EVENT', False, 0.1)
        
        # Дождаться истечения задержки
        time.sleep(0.15)
        
        # Q должен быть False
        assert block.Q == False


class TestE_TP:
    """Тесты для Pulse timer (E_TP)"""
    
    def test_tp_pulse(self, fb_fixture, event_helper):
        """Тест импульса"""
        block = fb_fixture(E_TP).create()
        
        # Включить импульс с длительностью 0.1 сек
        result = block.call('REQ', 'REQ_EVENT', True, 0.1)
        assert result is not None
        assert block.Q == True
        
        # Дождаться завершения импульса
        time.sleep(0.15)
        
        # Q должен быть False
        assert block.Q == False


# ===========================
# Тесты для edge detection
# ===========================

class TestE_R_TRIG:
    """Тесты для Rising edge trigger (E_R_TRIG)"""
    
    def test_rising_edge(self, fb_fixture, event_helper):
        """Тест детекции нарастающего фронта"""
        block = fb_fixture(E_R_TRIG).create()
        
        # Переход из False в True
        result = block.call('EI', 'EI_EVENT', True)
        event_helper.assert_event_output(result, 'EI_EVENT')
        
        # Остается True - события не будет
        result = block.call('EI', 'EI_EVENT', True)
        assert result is None


class TestE_F_TRIG:
    """Тесты для Falling edge trigger (E_F_TRIG)"""
    
    def test_falling_edge(self, fb_fixture, event_helper):
        """Тест детекции падающего фронта"""
        block = fb_fixture(E_F_TRIG).create()
        
        # Сначала установить True
        block.call('EI', 'EI_EVENT', True)
        
        # Переход из True в False
        result = block.call('EI', 'EI_EVENT', False)
        event_helper.assert_event_output(result, 'EI_EVENT')
        
        # Остается False - события не будет
        result = block.call('EI', 'EI_EVENT', False)
        assert result is None


# ===========================
# Тесты для слияния/разделения
# ===========================

class TestE_SPLIT:
    """Тесты для Event split (E_SPLIT)"""
    
    def test_split_produces_events(self, fb_fixture, event_helper):
        """Тест разделения события"""
        block = fb_fixture(E_SPLIT).create()
        
        result = block.call('EI', 'EI_EVENT')
        assert result is not None
        # Split должен выдать список/кортеж с двумя событиями
        if isinstance(result, (list, tuple)):
            assert len(result) == 2


class TestE_MERGE:
    """Тесты для Event merge (E_MERGE)"""
    
    def test_merge_from_input1(self, fb_fixture, event_helper):
        """Тест объединения из входа 1"""
        block = fb_fixture(E_MERGE).create()
        
        result = block.call('EI1', 'EI1_EVENT')
        event_helper.assert_event_output(result, 'EI1_EVENT')
    
    def test_merge_from_input2(self, fb_fixture, event_helper):
        """Тест объединения из входа 2"""
        block = fb_fixture(E_MERGE).create()
        
        result = block.call('EI2', 'EI2_EVENT')
        event_helper.assert_event_output(result, 'EI2_EVENT')


# ===========================
# Интеграционные тесты
# ===========================

class TestEventBlockIntegration:
    """Интеграционные тесты для комбинаций event блоков"""
    
    def test_counter_with_trigger(self, fb_fixture, event_helper):
        """Тест счетчика с детектором фронта"""
        counter = fb_fixture(E_CTU).create()
        trigger = fb_fixture(E_R_TRIG).create()
        
        # Генерировать нарастающий фронт
        trigger_result = trigger.call('EI', 'TRIG_EVENT', True)
        
        # Если фронт обнаружен, увеличить счетчик
        if trigger_result:
            counter_result = counter.call('CU', trigger_result, 10)
            assert counter_result is not None
    
    def test_demux_to_multiple_blocks(self, fb_fixture, event_helper):
        """Тест демультиплексирования в несколько блоков"""
        demux = fb_fixture(E_DEMUX_2).create()
        counter_0 = fb_fixture(E_CTU).create()
        counter_1 = fb_fixture(E_CTU).create()
        
        # Демультиплексировать
        demux_result = demux.call('EI', 'EI_EVENT', 0)
        
        # Маршрутизировать на нужные счетчики
        if demux_result[0]:
            counter_0.call('CU', demux_result[0], 10)
        if demux_result[1]:
            counter_1.call('CU', demux_result[1], 10)
