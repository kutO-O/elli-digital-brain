"""
Тесты для синапсов.
"""

import pytest
import numpy as np
from brain.synapses import STDPSynapse, STPSynapse, DopamineSTDPSynapse


class TestSTDPSynapse:
    """STDP synapse tests."""
    
    def test_initialization(self):
        """Синапс инициализируется."""
        synapse = STDPSynapse()
        
        assert synapse.weight == 0.5
        assert synapse.pre_trace == 0.0
        assert synapse.post_trace == 0.0
    
    def test_transmit(self):
        """Передача сигнала."""
        synapse = STDPSynapse(initial_weight=0.5)
        
        output = synapse.transmit(pre_spike=1.0, time=10.0)
        
        assert output == 0.5  # weight * spike
        assert synapse.pre_trace == 1.0
    
    def test_ltp_potentiation(self):
        """LTP: пре спайкает ПЕРЕД post → усиление."""
        synapse = STDPSynapse(initial_weight=0.5, a_plus=0.1, a_minus=0.1)
        
        initial_weight = synapse.weight
        
        # Pre spike first
        synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=0.0)
        
        # Post spike after (10ms later)
        for _ in range(10):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=1.0)
        synapse.update_weight(pre_spike=0.0, post_spike=1.0, time=10.0)
        
        # Вес должен увеличиться
        assert synapse.weight > initial_weight
    
    def test_ltd_depression(self):
        """LTD: post спайкает ПЕРЕД pre → ослабление."""
        synapse = STDPSynapse(initial_weight=0.5, a_plus=0.1, a_minus=0.1)
        
        initial_weight = synapse.weight
        
        # Post spike first
        synapse.update_weight(pre_spike=0.0, post_spike=1.0, time=0.0)
        
        # Pre spike after (10ms later)
        for _ in range(10):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=1.0)
        synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=10.0)
        
        # Вес должен уменьшиться
        assert synapse.weight < initial_weight
    
    def test_weight_bounds(self):
        """Вес остаётся в границах."""
        synapse = STDPSynapse(
            initial_weight=0.9,
            min_weight=0.0,
            max_weight=1.0,
            a_plus=0.5
        )
        
        # Много LTP
        for _ in range(10):
            synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=0.0)
            synapse.update_weight(pre_spike=0.0, post_spike=1.0, time=5.0)
        
        # Не должен превысить max
        assert synapse.weight <= 1.0
        assert synapse.weight >= 0.0


class TestSTPSynapse:
    """STP synapse tests."""
    
    def test_initialization(self):
        """Синапс инициализируется."""
        synapse = STPSynapse()
        
        assert synapse.weight == 0.5
        assert synapse.u == synapse.U
        assert synapse.x == 1.0
    
    def test_facilitating_type(self):
        """
Facilitating синапс усиливается."""
        synapse = STPSynapse(synapse_type='facilitating')
        
        outputs = []
        for _ in range(5):
            output = synapse.transmit(pre_spike=1.0, time=0.0)
            outputs.append(output)
            synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=0.0, dt=10.0)
        
        # Выход должен увеличиваться
        assert outputs[-1] > outputs[0]
    
    def test_depressing_type(self):
        """
Depressing синапс ослабляется."""
        synapse = STPSynapse(synapse_type='depressing')
        
        outputs = []
        for _ in range(5):
            output = synapse.transmit(pre_spike=1.0, time=0.0)
            outputs.append(output)
            synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=0.0, dt=1.0)
        
        # Выход должен уменьшаться
        assert outputs[-1] < outputs[0]
    
    def test_recovery(self):
        """Синапс восстанавливается."""
        synapse = STPSynapse(synapse_type='depressing')
        
        # Depression
        for _ in range(5):
            synapse.transmit(pre_spike=1.0, time=0.0)
        
        x_depressed = synapse.x
        
        # Recovery (no spikes)
        for _ in range(100):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=10.0)
        
        # x должен восстановиться
        assert synapse.x > x_depressed


class TestDopamineSTDPSynapse:
    """Dopamine-modulated STDP tests."""
    
    def test_initialization(self):
        """Синапс инициализируется."""
        synapse = DopamineSTDPSynapse()
        
        assert synapse.weight == 0.5
        assert synapse.dopamine_level == synapse.baseline_dopamine
        assert synapse.eligibility == 0.0
    
    def test_set_dopamine(self):
        """Установка дофамина."""
        synapse = DopamineSTDPSynapse(baseline_dopamine=0.5)
        
        synapse.set_dopamine(0.8)
        assert synapse.dopamine_level == 0.8
        
        synapse.set_dopamine(1.5)  # Выше максимума
        assert synapse.dopamine_level == 1.0  # Clipped
    
    def test_reward_strengthens(self):
        """
Reward (высокий dopamine) усиливает синапс."""
        synapse = DopamineSTDPSynapse(
            initial_weight=0.5,
            baseline_dopamine=0.5,
            a_plus=0.1
        )
        
        initial_weight = synapse.weight
        
        # Создать eligibility trace (pre раньше post)
        synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=0.0)
        for _ in range(5):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=1.0)
        synapse.update_weight(pre_spike=0.0, post_spike=1.0, time=5.0)
        
        # Дать reward
        synapse.set_dopamine(0.9)
        
        # Обновить
        for _ in range(10):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=1.0)
        
        # Вес должен увеличиться
        assert synapse.weight > initial_weight
    
    def test_punishment_weakens(self):
        """
Punishment (низкий dopamine) ослабляет синапс."""
        synapse = DopamineSTDPSynapse(
            initial_weight=0.5,
            baseline_dopamine=0.5,
            a_plus=0.1
        )
        
        initial_weight = synapse.weight
        
        # Создать eligibility trace
        synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=0.0)
        for _ in range(5):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=1.0)
        synapse.update_weight(pre_spike=0.0, post_spike=1.0, time=5.0)
        
        # Дать punishment
        synapse.set_dopamine(0.1)
        
        # Обновить
        for _ in range(10):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=1.0)
        
        # Вес должен уменьшиться
        assert synapse.weight < initial_weight
    
    def test_dopamine_decay(self):
        """
Dopamine decay к baseline."""
        synapse = DopamineSTDPSynapse(baseline_dopamine=0.5)
        
        synapse.set_dopamine(0.9)
        
        # Decay
        for _ in range(100):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=10.0)
        
        # Должен быть близок к baseline
        assert abs(synapse.dopamine_level - 0.5) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
