"""
STP (Short-Term Plasticity) синапс.

Краткосрочная пластичность:

1. **Facilitation** (усиление):
   - Повторные спайки УСИЛИВАЮТ передачу
   - Характерно для возбуждающих синапсов

2. **Depression** (ослабление):
   - Повторные спайки ОСЛАБЛЯЮТ передачу
   - Характерно для тормозных синапсов

Длится сотни миллисекунд (в отличие от STDP).
"""

import numpy as np
from .synapse_base import SynapseBase


class STPSynapse(SynapseBase):
    """
    STP синапс с facilitation и depression.
    
    Динамически изменяет силу передачи.
    """
    
    def __init__(
        self,
        initial_weight: float = 0.5,
        min_weight: float = 0.0,
        max_weight: float = 1.0,
        delay: float = 1.0,
        U: float = 0.5,              # Вероятность высвобождения
        tau_d: float = 200.0,        # Время depression (ms)
        tau_f: float = 600.0,        # Время facilitation (ms)
        synapse_type: str = 'mixed', # 'facilitating', 'depressing', 'mixed'
        synapse_id: str = None
    ):
        """
        Args:
            initial_weight: Начальный вес
            min_weight: Минимальный вес
            max_weight: Максимальный вес
            delay: Задержка
            U: Вероятность высвобождения нейротрансмиттера
            tau_d: Время восстановления от depression
            tau_f: Время восстановления от facilitation
            synapse_type: Тип ('facilitating', 'depressing', 'mixed')
            synapse_id: ID
        """
        super().__init__(initial_weight, min_weight, max_weight, delay, synapse_id)
        
        # STP параметры
        self.U = U  # Utilization parameter
        self.tau_d = tau_d  # Depression time constant
        self.tau_f = tau_f  # Facilitation time constant
        self.synapse_type = synapse_type
        
        # Переменные состояния
        self.u = U  # Текущая utilization
        self.x = 1.0  # Доступные ресурсы (1 = полностью)
        
        # Предопределённые типы
        if synapse_type == 'facilitating':
            self.U = 0.15
            self.tau_f = 750.0
            self.tau_d = 50.0
        elif synapse_type == 'depressing':
            self.U = 0.5
            self.tau_f = 20.0
            self.tau_d = 750.0
    
    def transmit(self, pre_spike: float, time: float) -> float:
        """
        Передать сигнал с STP.
        
        Args:
            pre_spike: Пресинаптический спайк
            time: Текущее время
            
        Returns:
            Выходной ток
        """
        if pre_spike > 0:
            # Увеличить u (facilitation)
            self.u += self.U * (1 - self.u)
            
            # Эффективный вес = weight * u * x
            effective_weight = self.weight * self.u * self.x
            
            # Уменьшить ресурсы (depression)
            self.x -= self.u * self.x
            
            self.last_pre_spike_time = time
            
            return effective_weight * pre_spike
        
        return 0.0
    
    def update_weight(
        self,
        pre_spike: float,
        post_spike: float,
        time: float,
        dt: float = 1.0
    ):
        """
        Обновить динамические переменные.
        """
        # Восстановление u к U
        self.u += (self.U - self.u) * dt / self.tau_f
        
        # Восстановление x к 1.0
        self.x += (1.0 - self.x) * dt / self.tau_d
        
        # Ограничить
        self.u = np.clip(self.u, 0.0, 1.0)
        self.x = np.clip(self.x, 0.0, 1.0)
    
    def get_state(self) -> dict:
        """Текущее состояние."""
        state = super().get_state()
        state.update({
            'u': self.u,
            'x': self.x,
            'U': self.U,
            'tau_d': self.tau_d,
            'tau_f': self.tau_f,
            'synapse_type': self.synapse_type,
        })
        return state
