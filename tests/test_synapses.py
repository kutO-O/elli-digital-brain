"""
Тесты для синапсов.
"""

import pytest
import numpy as np
from brain.synapses import STDPSynapse, STPSynapse, DopamineModulatedSynapse


class TestSTDPSynapse:
    """Tests for STDP synapse."""
    
    def test_initialization(self):
        """Синапс инициализируется правильно."""
        synapse = STDPSynapse(weight=1.0)
        
        assert synapse.weight == 1.0
        assert synapse.pre_trace == 0.0
        assert synapse.post_trace == 0.0
    
    def test_ltp_causality(self):
        """
LTP: pre перед post -> усиление."""
        synapse = STDPSynapse(weight=1.0, a_plus=0.1, a_minus=0.1)
        
        initial_weight = synapse.weight
        
        # Pre спайк
        synapse.update(pre_spike=1.0, post_spike=0.0, dt=1.0)
        
        # 5ms задержка
        for _ in range(5):
            synapse.update(pre_spike=0.0, post_spike=0.0, dt=1.0)
        
        # Post спайк
        synapse.update(pre_spike=0.0, post_spike=1.0, dt=1.0)
        
        # Вес должен увеличиться
        assert synapse.weight > initial_weight
    
    def test_ltd_anti_causality(self):
        """
LTD: post перед pre -> ослабление."""
        synapse = STDPSynapse(weight=1.0, a_plus=0.1, a_minus=0.1)
        
        initial_weight = synapse.weight
        
        # Post спайк
        synapse.update(pre_spike=0.0, post_spike=1.0, dt=1.0)
        
        # 5ms задержка
        for _ in range(5):
            synapse.update(pre_spike=0.0, post_spike=0.0, dt=1.0)
        
        # Pre спайк
        synapse.update(pre_spike=1.0, post_spike=0.0, dt=1.0)
        
        # Вес должен уменьшиться
        assert synapse.weight < initial_weight
    
    def test_weight_clipping(self):
        """Вес ограничен пределами."""
        synapse = STDPSynapse(weight=1.0, w_min=0.0, w_max=2.0, a_plus=1.0)
        
        # Много LTP
        for _ in range(100):
            synapse.update(pre_spike=1.0, post_spike=0.0, dt=1.0)
            for _ in range(5):
                synapse.update(pre_spike=0.0, post_spike=0.0, dt=1.0)
            synapse.update(pre_spike=0.0, post_spike=1.0, dt=1.0)
        
        # Не должен превышать max
        assert synapse.weight <= 2.0
        assert synapse.weight >= 0.0
    
    def test_stdp_window(self):
        """STDP окно имеет правильную форму."""
        synapse = STDPSynapse()
        
        window = synapse.get_stdp_window(delta_t_range=(-50, 50))
        
        assert 'delta_t' in window
        assert 'delta_w' in window
        assert len(window['delta_t']) == 200
        
        # Положительная часть (LTP)
        positive_idx = window['delta_t'] > 0
        assert np.all(window['delta_w'][positive_idx] > 0)
        
        # Отрицательная часть (LTD)
        negative_idx = window['delta_t'] < 0
        assert np.all(window['delta_w'][negative_idx] < 0)


class TestSTPSynapse:
    """Tests for STP synapse."""
    
    def test_initialization(self):
        """Синапс инициализируется правильно."""
        synapse = STPSynapse(weight=1.0, U=0.5)
        
        assert synapse.weight == 1.0
        assert synapse.U == 0.5
        assert synapse.x == 1.0
        assert synapse.u == 0.5
    
    def test_depression(self):
        """Depression: эффективный вес уменьшается."""
        synapse = STPSynapse.create_depressing()
        
        initial_effective = synapse.u * synapse.x
        
        # Несколько спайков подряд
        for _ in range(5):
            synapse.update(pre_spike=1.0, dt=10.0)
        
        final_effective = synapse.u * synapse.x
        
        # Эффективный вес должен уменьшиться
        assert final_effective < initial_effective
    
    def test_facilitation(self):
        """Facilitation: u увеличивается."""
        synapse = STPSynapse.create_facilitating()
        
        initial_u = synapse.u
        
        # Несколько спайков
        for _ in range(3):
            synapse.update(pre_spike=1.0, dt=10.0)
        
        # u должно увеличиться
        assert synapse.u > initial_u
    
    def test_recovery(self):
        """Ресурсы восстанавливаются."""
        synapse = STPSynapse(U=0.5, tau_rec=50.0)
        
        # Истощить ресурсы
        synapse.update(pre_spike=1.0)
        depleted_x = synapse.x
        
        # Подождать
        for _ in range(200):
            synapse.update(pre_spike=0.0, dt=1.0)
        
        # Ресурсы должны восстановиться
        assert synapse.x > depleted_x
        assert synapse.x > 0.9  # Почти полное восстановление


class TestDopamineModulatedSynapse:
    """Tests for dopamine-modulated synapse."""
    
    def test_initialization(self):
        """Синапс инициализируется."""
        synapse = DopamineModulatedSynapse(weight=1.0)
        
        assert synapse.weight == 1.0
        assert synapse.eligibility == 0.0
    
    def test_reward_learning(self):
        """Положительная награда усиливает синапс."""
        synapse = DopamineModulatedSynapse(weight=1.0, a_plus=0.1)
        
        initial_weight = synapse.weight
        
        # Causal спайки (создаёт eligibility)
        synapse.update(pre_spike=1.0, post_spike=0.0, dopamine=0.0, dt=1.0)
        for _ in range(5):
            synapse.update(pre_spike=0.0, post_spike=0.0, dopamine=0.0, dt=1.0)
        synapse.update(pre_spike=0.0, post_spike=1.0, dopamine=0.0, dt=1.0)
        
        # Награда!
        for _ in range(50):
            synapse.update(pre_spike=0.0, post_spike=0.0, dopamine=1.0, dt=1.0)
        
        # Вес должен увеличиться
        assert synapse.weight > initial_weight
    
    def test_punishment_learning(self):
        """Отрицательная награда ослабляет синапс."""
        synapse = DopamineModulatedSynapse(weight=1.0, a_plus=0.1)
        
        initial_weight = synapse.weight
        
        # Causal спайки
        synapse.update(pre_spike=1.0, post_spike=0.0, dopamine=0.0, dt=1.0)
        for _ in range(5):
            synapse.update(pre_spike=0.0, post_spike=0.0, dopamine=0.0, dt=1.0)
        synapse.update(pre_spike=0.0, post_spike=1.0, dopamine=0.0, dt=1.0)
        
        # Наказание!
        for _ in range(50):
            synapse.update(pre_spike=0.0, post_spike=0.0, dopamine=-1.0, dt=1.0)
        
        # Вес должен уменьшиться
        assert synapse.weight < initial_weight
    
    def test_no_reward_no_change(self):
        """Без дофамина изменения минимальны."""
        synapse = DopamineModulatedSynapse(weight=1.0, a_plus=0.1)
        
        initial_weight = synapse.weight
        
        # Causal спайки без дофамина
        for _ in range(10):
            synapse.update(pre_spike=1.0, post_spike=0.0, dopamine=0.0, dt=1.0)
            for _ in range(5):
                synapse.update(pre_spike=0.0, post_spike=0.0, dopamine=0.0, dt=1.0)
            synapse.update(pre_spike=0.0, post_spike=1.0, dopamine=0.0, dt=1.0)
        
        # Изменение должно быть минимальным
        assert abs(synapse.weight - initial_weight) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
