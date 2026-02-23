"""
Dopamine-modulated STDP.

Синаптическая пластичность, модулируемая дофамином.

Используется для:
- Reward learning (обучение с подкреплением)
- Motivation (мотивация)
- Goal-directed behavior (целенаправленное поведение)

Dopamine сигнализирует:
- Reward prediction error (RPE)
- Неожиданное вознаграждение → усиление
- Отсутствие ожидаемого вознаграждения → ослабление
"""

import numpy as np
from .stdp import STDPSynapse


class DopamineSTDPSynapse(STDPSynapse):
    """
    STDP с дофаминовой модуляцией.
    
    Изменение веса модулируется уровнем дофамина.
    """
    
    def __init__(
        self,
        initial_weight: float = 0.5,
        min_weight: float = 0.0,
        max_weight: float = 1.0,
        delay: float = 1.0,
        tau_plus: float = 20.0,
        tau_minus: float = 20.0,
        a_plus: float = 0.01,
        a_minus: float = 0.01,
        tau_dopamine: float = 200.0,   # Постоянная дофамина
        baseline_dopamine: float = 0.5, # Базовый уровень
        synapse_id: str = None
    ):
        """
        Args:
            initial_weight: Начальный вес
            min_weight: Минимальный вес
            max_weight: Максимальный вес
            delay: Задержка
            tau_plus: Временная константа LTP
            tau_minus: Временная константа LTD
            a_plus: Амплитуда LTP
            a_minus: Амплитуда LTD
            tau_dopamine: Время decay дофамина
            baseline_dopamine: Базовый уровень дофамина
            synapse_id: ID
        """
        super().__init__(
            initial_weight, min_weight, max_weight, delay,
            tau_plus, tau_minus, a_plus, a_minus, synapse_id
        )
        
        # Dopamine параметры
        self.tau_dopamine = tau_dopamine
        self.baseline_dopamine = baseline_dopamine
        self.dopamine_level = baseline_dopamine
        
        # Eligibility trace (след допустимости)
        self.eligibility = 0.0
        self.tau_eligibility = 1000.0  # Долгоживущий след
    
    def set_dopamine(self, dopamine: float):
        """
        Установить уровень дофамина.
        
        Args:
            dopamine: Уровень (0.0 - 1.0)
                     > baseline = reward
                     < baseline = punishment
        """
        self.dopamine_level = np.clip(dopamine, 0.0, 1.0)
    
    def update_weight(
        self,
        pre_spike: float,
        post_spike: float,
        time: float,
        dt: float = 1.0
    ):
        """
        Обновить вес с dopamine modulation.
        
        3-factor learning rule:
        dw = dopamine * eligibility_trace
        """
        # Decay traces
        self.pre_trace *= np.exp(-dt / self.tau_plus)
        self.post_trace *= np.exp(-dt / self.tau_minus)
        self.eligibility *= np.exp(-dt / self.tau_eligibility)
        
        # Decay dopamine
        self.dopamine_level += (self.baseline_dopamine - self.dopamine_level) * dt / self.tau_dopamine
        
        # Обновить eligibility trace (как STDP)
        if pre_spike > 0:
            self.pre_trace = 1.0
            self.eligibility -= self.a_minus * self.post_trace
        
        if post_spike > 0:
            self.post_trace = 1.0
            self.eligibility += self.a_plus * self.pre_trace
        
        # Дофаминовая модуляция
        # RPE (Reward Prediction Error)
        rpe = self.dopamine_level - self.baseline_dopamine
        
        # Изменение веса
        delta_w = rpe * self.eligibility * dt
        self.weight += delta_w
        
        # Ограничить
        self.clip_weight()
        
        # Записать
        if len(self.weight_history) == 0 or abs(self.weight_history[-1] - self.weight) > 1e-6:
            self.weight_history.append(self.weight)
    
    def get_state(self) -> dict:
        """Текущее состояние."""
        state = super().get_state()
        state.update({
            'dopamine_level': self.dopamine_level,
            'baseline_dopamine': self.baseline_dopamine,
            'eligibility': self.eligibility,
        })
        return state
