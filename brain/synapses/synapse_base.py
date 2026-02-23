"""
Базовый класс для всех синапсов.
"""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


class SynapseBase(ABC):
    """
    Абстрактный базовый класс синапса.
    
    Синапс соединяет два нейрона и может:
    - Усиливаться/ослабляться (пластичность)
    - Передавать сигнал с задержкой
    - Изменять свою силу в зависимости от активности
    """
    
    def __init__(
        self,
        initial_weight: float = 0.5,
        min_weight: float = 0.0,
        max_weight: float = 1.0,
        delay: float = 1.0,
        synapse_id: Optional[str] = None
    ):
        """
        Args:
            initial_weight: Начальный вес синапса
            min_weight: Минимальный вес
            max_weight: Максимальный вес
            delay: Задержка передачи (ms)
            synapse_id: Уникальный идентификатор
        """
        self.synapse_id = synapse_id or f"synapse_{id(self)}"
        self.weight = initial_weight
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.delay = delay
        
        # История
        self.weight_history = [initial_weight]
        self.last_pre_spike_time = -np.inf
        self.last_post_spike_time = -np.inf
        
    @abstractmethod
    def transmit(self, pre_spike: float, time: float) -> float:
        """
        Передать сигнал через синапс.
        
        Args:
            pre_spike: Спайк пресинаптического нейрона (0 или 1)
            time: Текущее время (ms)
            
        Returns:
            Выходной сигнал (ток)
        """
        pass
    
    def update_weight(
        self,
        pre_spike: float,
        post_spike: float,
        time: float
    ):
        """
        Обновить вес синапса (пластичность).
        
        Переопределяется в подклассах (STDP, STP, и т.д.).
        """
        pass
    
    def clip_weight(self):
        """Ограничить вес в допустимых пределах."""
        self.weight = np.clip(self.weight, self.min_weight, self.max_weight)
    
    def get_state(self) -> dict:
        """Текущее состояние синапса."""
        return {
            'synapse_id': self.synapse_id,
            'weight': self.weight,
            'min_weight': self.min_weight,
            'max_weight': self.max_weight,
            'delay': self.delay,
        }
    
    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"weight={self.weight:.3f}, "
            f"delay={self.delay:.1f}ms)"
        )
