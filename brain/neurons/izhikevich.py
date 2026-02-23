"""
Izhikevich нейрон.

Более биологически точная модель, чем LIF.
Может имитировать 20+ типов реальных нейронов:
- Regular Spiking (RS)
- Fast Spiking (FS)
- Intrinsically Bursting (IB)
- Chattering (CH)
- Low-Threshold Spiking (LTS)
- И другие...

Основана на работе Eugene Izhikevich (2003).
"""

import numpy as np
from typing import Optional, Dict
from .neuron_base import NeuronBase


class IzhikevichNeuron(NeuronBase):
    """
    Izhikevich нейрон.
    
    Уравнения:
    dv/dt = 0.04*v^2 + 5*v + 140 - u + I
    du/dt = a*(b*v - u)
    
    Если v >= 30 mV, то:
        v = c
        u = u + d
    
    Параметры:
    a - скорость восстановления u
    b - чувствительность u к v
    c - reset значение v после спайка
    d - reset изменение u после спайка
    """
    
    # Предопределённые типы нейронов
    NEURON_TYPES = {
        # Cortical neurons
        'RS': {'a': 0.02, 'b': 0.2, 'c': -65, 'd': 8, 'name': 'Regular Spiking'},
        'IB': {'a': 0.02, 'b': 0.2, 'c': -55, 'd': 4, 'name': 'Intrinsically Bursting'},
        'CH': {'a': 0.02, 'b': 0.2, 'c': -50, 'd': 2, 'name': 'Chattering'},
        'FS': {'a': 0.1, 'b': 0.2, 'c': -65, 'd': 2, 'name': 'Fast Spiking'},
        'LTS': {'a': 0.02, 'b': 0.25, 'c': -65, 'd': 2, 'name': 'Low-Threshold Spiking'},
        
        # Thalamic neurons
        'TC': {'a': 0.02, 'b': 0.25, 'c': -65, 'd': 0.05, 'name': 'Thalamo-Cortical'},
        'RZ': {'a': 0.1, 'b': 0.26, 'c': -65, 'd': 2, 'name': 'Resonator'},
        
        # Other types
        'REB': {'a': 0.03, 'b': 0.25, 'c': -60, 'd': 4, 'name': 'Rebound Burst'},
        'RES': {'a': 0.1, 'b': 0.25, 'c': -65, 'd': 2, 'name': 'Rebound Spike'},
        'THR': {'a': 0.02, 'b': -0.1, 'c': -55, 'd': 6, 'name': 'Threshold Variability'},
        'BI': {'a': 0.05, 'b': 0.26, 'c': -60, 'd': 0, 'name': 'Bistability'},
        'DAP': {'a': 1.0, 'b': 0.2, 'c': -60, 'd': -21, 'name': 'Depolarizing Afterpotential'},
        'AC': {'a': 0.02, 'b': 1.0, 'c': -55, 'd': 4, 'name': 'Accommodation'},
        'IH': {'a': 0.02, 'b': -0.1, 'c': -55, 'd': 6, 'name': 'Inhibition-Induced Spiking'},
        'IIB': {'a': 0.02, 'b': -0.1, 'c': -55, 'd': 0, 'name': 'Inhibition-Induced Bursting'},
        
        # Specialized behaviors
        'MIXED': {'a': 0.02, 'b': 0.2, 'c': -55, 'd': 4, 'name': 'Mixed Mode'},
        'SPIKE_LAT': {'a': 0.03, 'b': 0.25, 'c': -60, 'd': 4, 'name': 'Spike Latency'},
        'SUBTHRESHOLD': {'a': 0.05, 'b': 0.26, 'c': -60, 'd': 0, 'name': 'Subthreshold Oscillation'},
        'RESONATOR': {'a': 0.1, 'b': 0.26, 'c': -60, 'd': -1, 'name': 'Resonator'},
        'INTEGRATOR': {'a': 0.02, 'b': -0.1, 'c': -55, 'd': 6, 'name': 'Integrator'},
        'REFRACTORY': {'a': 0.1, 'b': 0.2, 'c': -65, 'd': 2, 'name': 'Refractory'},
    }
    
    def __init__(
        self,
        a: float = 0.02,
        b: float = 0.2,
        c: float = -65.0,
        d: float = 8.0,
        v_init: float = -65.0,
        u_init: Optional[float] = None,
        neuron_type: Optional[str] = None,
        neuron_id: Optional[str] = None
    ):
        """
        Args:
            a: Скорость восстановления (обычно 0.02)
            b: Чувствительность восстановления (обычно 0.2)
            c: Reset значение мембранного потенциала (обычно -65 mV)
            d: Reset изменение восстановительной переменной (обычно 8)
            v_init: Начальное значение v
            u_init: Начальное значение u (по умолчанию b*v_init)
            neuron_type: Предопределённый тип нейрона (см. NEURON_TYPES)
            neuron_id: ID нейрона
        """
        super().__init__(neuron_id)
        
        # Если указан тип, использовать параметры из NEURON_TYPES
        if neuron_type:
            if neuron_type not in self.NEURON_TYPES:
                raise ValueError(
                    f"Unknown neuron type: {neuron_type}. "
                    f"Available: {list(self.NEURON_TYPES.keys())}"
                )
            params = self.NEURON_TYPES[neuron_type]
            a = params['a']
            b = params['b']
            c = params['c']
            d = params['d']
            self.type_name = params['name']
        else:
            self.type_name = "Custom"
        
        # Параметры модели
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
        # Состояние
        self.v = v_init  # Мембранный потенциал
        self.u = u_init if u_init is not None else b * v_init  # Восстановительная переменная
        self.membrane_potential = self.v  # Для совместимости с базовым классом
        
        # Порог спайка
        self.spike_threshold = 30.0  # mV
        
    def step(self, input_current: float, dt: float = 1.0) -> float:
        """
        Один временной шаг.
        
        Args:
            input_current: Входной ток (pA)
            dt: Временной шаг (ms)
            
        Returns:
            1.0 если спайк, 0.0 иначе
        """
        self.time_step += dt
        
        # Интеграция уравнений (метод Эйлера с внутренними шагами)
        # Для стабильности делаем несколько маленьких шагов
        internal_steps = int(dt)
        internal_dt = dt / internal_steps if internal_steps > 0 else dt
        
        spike = 0.0
        
        for _ in range(max(1, internal_steps)):
            # Уравнение для v
            dv = (0.04 * self.v**2 + 5 * self.v + 140 - self.u + input_current) * internal_dt
            
            # Уравнение для u
            du = self.a * (self.b * self.v - self.u) * internal_dt
            
            # Обновление
            self.v += dv
            self.u += du
            
            # Проверка спайка
            if self.v >= self.spike_threshold:
                spike = 1.0
                self.v = self.c  # Reset v
                self.u += self.d  # Reset u
                self.spike_history.append(self.time_step)
        
        # Обновить для совместимости
        self.membrane_potential = self.v
        
        return spike
    
    def get_state(self) -> Dict:
        """Текущее состояние нейрона."""
        return {
            'neuron_id': self.neuron_id,
            'type': self.type_name,
            'v': self.v,
            'u': self.u,
            'spike_count': len(self.spike_history),
            'spike_rate': self.get_spike_rate(),
            'parameters': {
                'a': self.a,
                'b': self.b,
                'c': self.c,
                'd': self.d,
            }
        }
    
    @classmethod
    def create_cortical_excitatory(cls, **kwargs) -> 'IzhikevichNeuron':
        """Создать возбуждающий кортикальный нейрон (RS)."""
        return cls(neuron_type='RS', **kwargs)
    
    @classmethod
    def create_cortical_inhibitory(cls, **kwargs) -> 'IzhikevichNeuron':
        """Создать тормозной кортикальный нейрон (FS)."""
        return cls(neuron_type='FS', **kwargs)
    
    @classmethod
    def create_bursting(cls, **kwargs) -> 'IzhikevichNeuron':
        """Создать bursting нейрон (IB)."""
        return cls(neuron_type='IB', **kwargs)
    
    def __repr__(self):
        return (
            f"IzhikevichNeuron(type={self.type_name}, "
            f"v={self.v:.1f}mV, u={self.u:.1f}, "
            f"spikes={len(self.spike_history)})"
        )
