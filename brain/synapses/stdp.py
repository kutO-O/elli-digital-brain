"""
STDP (Spike-Timing-Dependent Plasticity).

"Neurons that fire together, wire together."

Если пресинаптический нейрон спайкает ПЕРЕД постсинаптическим,
синапс усиливается (LTP - Long-Term Potentiation).

Если пресинаптический спайкает ПОСЛЕ постсинаптического,
синапс ослабляется (LTD - Long-Term Depression).

Это основа обучения в мозге!
"""

import numpy as np
from typing import Optional
from .synapse_base import SynapseBase


class STDPSynapse(SynapseBase):
    """
    STDP синапс с временным окном.
    
    Параметры основаны на экспериментальных данных
    из гиппокампа и коры мозга.
    """
    
    def __init__(
        self,
        weight: float = 1.0,
        a_plus: float = 0.01,        # Амплитуда LTP
        a_minus: float = 0.01,       # Амплитуда LTD
        tau_plus: float = 20.0,      # Временное окно LTP (ms)
        tau_minus: float = 20.0,     # Временное окно LTD (ms)
        w_min: float = 0.0,
        w_max: float = 2.0,
        synapse_id: Optional[str] = None
    ):
        """
        Args:
            weight: Начальный вес
            a_plus: Амплитуда усиления (LTP)
            a_minus: Амплитуда ослабления (LTD)
            tau_plus: Временная константа для LTP
            tau_minus: Временная константа для LTD
            w_min: Минимальный вес
            w_max: Максимальный вес
            synapse_id: ID синапса
        """
        super().__init__(
            weight=weight,
            min_weight=w_min,
            max_weight=w_max,
            synapse_id=synapse_id
        )
        
        # STDP параметры
        self.a_plus = a_plus
        self.a_minus = a_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        
        # Следы активности (traces)
        self.pre_trace = 0.0   # След пресинаптической активности
        self.post_trace = 0.0  # След постсинаптической активности
        
        # История спайков для точного STDP
        self.pre_spike_times = []
        self.post_spike_times = []
        self.max_history = 100  # Хранить последние 100 спайков
        
    def update(
        self,
        pre_spike: float,
        post_spike: float,
        dt: float = 1.0
    ) -> float:
        """
        Обновить вес на основе STDP правила.
        
        Args:
            pre_spike: Спайк пресинаптического нейрона (0 или 1)
            post_spike: Спайк постсинаптического нейрона (0 или 1)
            dt: Временной шаг (ms)
            
        Returns:
            Изменение веса
        """
        self.time_step += dt
        
        delta_w = 0.0
        
        # Обновить следы (exponential decay)
        self.pre_trace *= np.exp(-dt / self.tau_plus)
        self.post_trace *= np.exp(-dt / self.tau_minus)
        
        # Постсинаптический спайк
        if post_spike > 0:
            self.post_spike_times.append(self.time_step)
            
            # LTP: усиление, если был недавний пре-спайк
            delta_w += self.a_plus * self.pre_trace
            
            # Обновить след
            self.post_trace = 1.0
        
        # Пресинаптический спайк
        if pre_spike > 0:
            self.pre_spike_times.append(self.time_step)
            
            # LTD: ослабление, если был недавний пост-спайк
            delta_w -= self.a_minus * self.post_trace
            
            # Обновить след
            self.pre_trace = 1.0
        
        # Применить изменение
        self.weight += delta_w
        self.clip_weight()
        
        # Сохранить в историю
        if len(self.weight_history) < 10000:  # Лимит памяти
            self.weight_history.append(self.weight)
        
        # Ограничить историю спайков
        if len(self.pre_spike_times) > self.max_history:
            self.pre_spike_times = self.pre_spike_times[-self.max_history:]
        if len(self.post_spike_times) > self.max_history:
            self.post_spike_times = self.post_spike_times[-self.max_history:]
        
        return delta_w
    
    def get_stdp_window(self, delta_t_range: tuple = (-100, 100)) -> dict:
        """
        Получить STDP окно (для визуализации).
        
        Args:
            delta_t_range: Диапазон времени (мс)
            
        Returns:
            Словарь с delta_t и delta_w
        """
        delta_t = np.linspace(delta_t_range[0], delta_t_range[1], 200)
        delta_w = np.zeros_like(delta_t)
        
        for i, dt in enumerate(delta_t):
            if dt > 0:  # Пре перед пост -> LTP
                delta_w[i] = self.a_plus * np.exp(-dt / self.tau_plus)
            else:  # Пост перед пре -> LTD
                delta_w[i] = -self.a_minus * np.exp(dt / self.tau_minus)
        
        return {'delta_t': delta_t, 'delta_w': delta_w}
    
    def get_state(self) -> dict:
        """Расширенное состояние с STDP информацией."""
        state = super().get_state()
        state.update({
            'pre_trace': self.pre_trace,
            'post_trace': self.post_trace,
            'recent_pre_spikes': len(self.pre_spike_times),
            'recent_post_spikes': len(self.post_spike_times),
        })
        return state
