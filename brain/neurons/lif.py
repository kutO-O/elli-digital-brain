"""
LIF (Leaky Integrate-and-Fire) нейрон.

Самая простая модель нейрона мозга:
- Мембранный потенциал "течёт" (decay)
- Интегрирует входной ток
- Генерирует спайк при превышении порога
- Сбрасывается после спайка

Используется как базовый строительный блок.
"""

import numpy as np
from .neuron_base import NeuronBase


class LIFNeuron(NeuronBase):
    """
    Leaky Integrate-and-Fire нейрон.
    
    Параметры близки к реальным корковым нейронам.
    """
    
    def __init__(
        self,
        threshold: float = 1.0,           # Порог спайка (mV)
        resting_potential: float = 0.0,   # Потенциал покоя (mV)
        reset_potential: float = 0.0,     # После спайка (mV)
        membrane_tau: float = 20.0,       # Постоянная времени (ms)
        refractory_period: float = 2.0,   # Рефрактерный период (ms)
        resistance: float = 1.0,          # Мембранное сопротивление (MΩ)
        neuron_id: str = None
    ):
        """
        Args:
            threshold: Порог генерации спайка
            resting_potential: Потенциал покоя
            reset_potential: Потенциал после спайка
            membrane_tau: Постоянная времени утечки
            refractory_period: Время невозбудимости после спайка
            resistance: Мембранное сопротивление
            neuron_id: ID нейрона
        """
        super().__init__(neuron_id)
        
        # Параметры
        self.threshold = threshold
        self.resting_potential = resting_potential
        self.reset_potential = reset_potential
        self.tau = membrane_tau
        self.refractory_period = refractory_period
        self.resistance = resistance
        
        # Состояние
        self.membrane_potential = resting_potential
        self.time_since_spike = float('inf')  # Время с последнего спайка
        
    def step(self, input_current: float, dt: float = 1.0) -> float:
        """
        Один шаг симуляции (обычно 1ms).
        
        Уравнение:
        dV/dt = (-(V - V_rest) + R*I) / tau
        
        Args:
            input_current: Входной ток в mA
            dt: Временной шаг в ms
            
        Returns:
            1.0 если спайк произошёл, 0.0 иначе
        """
        self.time_step += dt
        self.time_since_spike += dt
        
        # Рефрактерный период — нейрон не реагирует
        if self.time_since_spike < self.refractory_period:
            return 0.0
        
        # Leak (утечка к потенциалу покоя)
        leak = -(self.membrane_potential - self.resting_potential) / self.tau
        
        # Input (входной ток через сопротивление)
        input_effect = self.resistance * input_current
        
        # Интеграция (метод Эйлера)
        dV = (leak + input_effect) * dt
        self.membrane_potential += dV
        
        # Проверка порога
        if self.membrane_potential >= self.threshold:
            # СПАЙК!
            self.membrane_potential = self.reset_potential
            self.time_since_spike = 0.0
            self.spike_history.append(self.time_step)
            return 1.0
        
        return 0.0
    
    def get_state(self) -> dict:
        """Текущее состояние нейрона."""
        return {
            'neuron_id': self.neuron_id,
            'membrane_potential': self.membrane_potential,
            'time_since_spike': self.time_since_spike,
            'spike_count': len(self.spike_history),
            'current_spike_rate': self.get_spike_rate(),
        }
    
    def __repr__(self):
        return (
            f"LIFNeuron(id={self.neuron_id}, "
            f"V={self.membrane_potential:.2f}mV, "
            f"spikes={len(self.spike_history)})"
        )
