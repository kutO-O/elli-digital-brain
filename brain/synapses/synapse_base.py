"""
Базовый класс для всех синапсов Элли.
"""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


class SynapseBase(ABC):
    """
    Абстрактный базовый класс синапса.
    
    Синапс = связь между двумя нейронами.
    Вес синапса определяет силу связи.
    """
    
    def __init__(
        self,
        weight: float = 1.0,
        min_weight: float = 0.0,
        max_weight: float = 10.0,
        synapse_id: Optional[str] = None
    ):
        """
        Args:
            weight: Начальный вес синапса
            min_weight: Минимальный вес
            max_weight: Максимальный вес
            synapse_id: ID синапса
        """
        self.synapse_id = synapse_id or f"synapse_{id(self)}"
        self.weight = weight
        self.min_weight = min_weight
        self.max_weight = max_weight
        
        # История
        self.weight_history = [weight]
        self.time_step = 0
        
    def transmit(self, presynaptic_spike: float) -> float:
        """
        Передать сигнал через синапс.
        
        Args:
            presynaptic_spike: Спайк от пресинаптического нейрона (0 или 1)
            
        Returns:
            Сила сигнала = weight * spike
        """
        return self.weight * presynaptic_spike
    
    @abstractmethod
    def update(
        self,
        pre_spike: float,
        post_spike: float,
        dt: float = 1.0
    ) -> float:
        """
        Обновить вес синапса на основе активности нейронов.
        
        Args:
            pre_spike: Спайк пресинаптического нейрона
            post_spike: Спайк постсинаптического нейрона
            dt: Временной шаг
            
        Returns:
            Изменение веса
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
            'age': self.time_step,
        }
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.synapse_id}, w={self.weight:.3f})"
