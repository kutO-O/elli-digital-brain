"""
STDP (Spike-Timing-Dependent Plasticity) синапс.

Hebbian learning: "Neurons that fire together, wire together"

Если пресинаптический нейрон спайкает ПЕРЕД постсинаптическим:
  → синапс УСИЛИВАЕТСЯ (LTP - Long-Term Potentiation)

Если пресинаптический нейрон спайкает ПОСЛЕ постсинаптического:
  → синапс ОСЛАБЛЯЕТСЯ (LTD - Long-Term Depression)

Это основа обучения в мозге.
"""

import numpy as np
from .synapse_base import SynapseBase


class STDPSynapse(SynapseBase):
    """
    STDP синапс с Hebbian learning.
    
    Вес изменяется в зависимости от разницы времени спайков.
    """
    
    def __init__(
        self,
        initial_weight: float = 0.5,
        min_weight: float = 0.0,
        max_weight: float = 1.0,
        delay: float = 1.0,
        tau_plus: float = 20.0,      # Постоянная LTP (ms)
        tau_minus: float = 20.0,     # Постоянная LTD (ms)
        a_plus: float = 0.01,        # Амплитуда LTP
        a_minus: float = 0.01,       # Амплитуда LTD
        synapse_id: str = None
    ):
        """
        Args:
            initial_weight: Начальный вес
            min_weight: Минимальный вес
            max_weight: Максимальный вес
            delay: Задержка передачи
            tau_plus: Временная константа LTP
            tau_minus: Временная константа LTD
            a_plus: Амплитуда усиления
            a_minus: Амплитуда ослабления
            synapse_id: ID синапса
        """
        super().__init__(initial_weight, min_weight, max_weight, delay, synapse_id)
        
        # STDP параметры
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        self.a_plus = a_plus
        self.a_minus = a_minus
        
        # Трейсы (экспоненциальные следы активности)
        self.pre_trace = 0.0   # След пресинаптического спайка
        self.post_trace = 0.0  # След постсинаптического спайка
        
    def transmit(self, pre_spike: float, time: float) -> float:
        """
        Передать сигнал.
        
        Args:
            pre_spike: Спайк пресинаптического нейрона
            time: Текущее время
            
        Returns:
            Выходной ток (weight * pre_spike)
        """
        if pre_spike > 0:
            self.last_pre_spike_time = time
            self.pre_trace = 1.0  # Reset trace
        
        return self.weight * pre_spike
    
    def update_weight(
        self,
        pre_spike: float,
        post_spike: float,
        time: float,
        dt: float = 1.0
    ):
        """
        Обновить вес по STDP.
        
        Args:
            pre_spike: Спайк пресинаптического нейрона
            post_spike: Спайк постсинаптического нейрона
            time: Текущее время
            dt: Временной шаг
        """
        # Decay traces
        self.pre_trace *= np.exp(-dt / self.tau_plus)
        self.post_trace *= np.exp(-dt / self.tau_minus)
        
        # Если пресинаптический спайк
        if pre_spike > 0:
            self.pre_trace = 1.0
            # LTD: пре спайкает ПОСЛЕ post
            self.weight -= self.a_minus * self.post_trace
        
        # Если постсинаптический спайк
        if post_spike > 0:
            self.post_trace = 1.0
            # LTP: пре спайкает ПЕРЕД post
            self.weight += self.a_plus * self.pre_trace
        
        # Ограничить вес
        self.clip_weight()
        
        # Записать в историю
        if len(self.weight_history) == 0 or self.weight_history[-1] != self.weight:
            self.weight_history.append(self.weight)
    
    def get_state(self) -> dict:
        """Текущее состояние."""
        state = super().get_state()
        state.update({
            'pre_trace': self.pre_trace,
            'post_trace': self.post_trace,
            'tau_plus': self.tau_plus,
            'tau_minus': self.tau_minus,
            'a_plus': self.a_plus,
            'a_minus': self.a_minus,
        })
        return state
