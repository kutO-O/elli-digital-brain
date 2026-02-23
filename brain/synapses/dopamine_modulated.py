"""
Dopamine-Modulated Synapse.

Синапс, модулируемый дофамином (система вознаграждения).

Дофамин усиливает/ослабляет синаптические изменения
в зависимости от награды или наказания.

Основа reinforcement learning в мозге.
"""

import numpy as np
from typing import Optional
from .stdp import STDPSynapse


class DopamineModulatedSynapse(STDPSynapse):
    """
    STDP синапс с модуляцией дофамином.
    
    Изменения веса применяются только при наличии дофаминового сигнала.
    Это позволяет мозгу учиться на основе вознаграждения.
    """
    
    def __init__(
        self,
        weight: float = 1.0,
        a_plus: float = 0.01,
        a_minus: float = 0.01,
        tau_plus: float = 20.0,
        tau_minus: float = 20.0,
        tau_eligibility: float = 1000.0,  # Eligibility trace decay
        dopamine_baseline: float = 0.0,
        w_min: float = 0.0,
        w_max: float = 2.0,
        synapse_id: Optional[str] = None
    ):
        """
        Args:
            weight: Начальный вес
            a_plus: Амплитуда LTP
            a_minus: Амплитуда LTD
            tau_plus: Временная константа LTP
            tau_minus: Временная константа LTD
            tau_eligibility: Время затухания eligibility trace
            dopamine_baseline: Базовый уровень дофамина
            w_min: Минимальный вес
            w_max: Максимальный вес
            synapse_id: ID синапса
        """
        super().__init__(
            weight=weight,
            a_plus=a_plus,
            a_minus=a_minus,
            tau_plus=tau_plus,
            tau_minus=tau_minus,
            w_min=w_min,
            w_max=w_max,
            synapse_id=synapse_id
        )
        
        # Dopamine параметры
        self.tau_eligibility = tau_eligibility
        self.dopamine_baseline = dopamine_baseline
        
        # Eligibility trace (временной след потенциального изменения)
        self.eligibility = 0.0
        
        # История дофамина
        self.dopamine_history = []
        
    def update(
        self,
        pre_spike: float,
        post_spike: float,
        dopamine: float = 0.0,
        dt: float = 1.0
    ) -> float:
        """
        Обновить вес с учётом дофамина.
        
        Args:
            pre_spike: Пресинаптический спайк
            post_spike: Постсинаптический спайк
            dopamine: Уровень дофамина (награда)
            dt: Временной шаг
            
        Returns:
            Изменение веса
        """
        self.time_step += dt
        
        # Decay eligibility trace
        self.eligibility *= np.exp(-dt / self.tau_eligibility)
        
        # Обновить следы активности
        self.pre_trace *= np.exp(-dt / self.tau_plus)
        self.post_trace *= np.exp(-dt / self.tau_minus)
        
        # Вычислить потенциальное изменение (как в обычном STDP)
        potential_delta_w = 0.0
        
        if post_spike > 0:
            self.post_spike_times.append(self.time_step)
            potential_delta_w += self.a_plus * self.pre_trace
            self.post_trace = 1.0
        
        if pre_spike > 0:
            self.pre_spike_times.append(self.time_step)
            potential_delta_w -= self.a_minus * self.post_trace
            self.pre_trace = 1.0
        
        # Добавить к eligibility trace
        self.eligibility += potential_delta_w
        
        # Применить изменение, модулированное дофамином
        dopamine_signal = dopamine - self.dopamine_baseline
        actual_delta_w = self.eligibility * dopamine_signal * dt / self.tau_eligibility
        
        self.weight += actual_delta_w
        self.clip_weight()
        
        # Сохранить историю
        if len(self.weight_history) < 10000:
            self.weight_history.append(self.weight)
        if len(self.dopamine_history) < 10000:
            self.dopamine_history.append(dopamine)
        
        # Ограничить историю спайков
        if len(self.pre_spike_times) > self.max_history:
            self.pre_spike_times = self.pre_spike_times[-self.max_history:]
        if len(self.post_spike_times) > self.max_history:
            self.post_spike_times = self.post_spike_times[-self.max_history:]
        
        return actual_delta_w
    
    def get_state(self) -> dict:
        """Расширенное состояние с дофамином."""
        state = super().get_state()
        state.update({
            'eligibility': self.eligibility,
            'recent_dopamine': self.dopamine_history[-10:] if self.dopamine_history else [],
        })
        return state
