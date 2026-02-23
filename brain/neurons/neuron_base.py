"""
Базовый класс для всех нейронов Элли.
"""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


class NeuronBase(ABC):
    """
    Абстрактный базовый класс нейрона.
    
    Все нейроны Элли наследуются отсюда.
    """
    
    def __init__(self, neuron_id: Optional[str] = None):
        """
        Args:
            neuron_id: Уникальный идентификатор нейрона
        """
        self.neuron_id = neuron_id or f"neuron_{id(self)}"
        self.membrane_potential = 0.0
        self.spike_history = []
        self.time_step = 0
        
    @abstractmethod
    def step(self, input_current: float, dt: float = 1.0) -> float:
        """
        Один временной шаг симуляции.
        
        Args:
            input_current: Входной ток (мА)
            dt: Временной шаг (мс)
            
        Returns:
            1.0 если спайк, 0.0 если нет
        """
        pass
    
    def reset(self):
        """Сброс состояния нейрона."""
        self.membrane_potential = 0.0
        self.spike_history = []
        self.time_step = 0
    
    def get_spike_rate(self, window_ms: int = 1000) -> float:
        """
        Частота спайков за последнее окно.
        
        Args:
            window_ms: Размер окна в мс
            
        Returns:
            Частота в Гц (спайки/сек)
        """
        if not self.spike_history:
            return 0.0
        
        recent_spikes = [
            t for t in self.spike_history
            if self.time_step - t <= window_ms
        ]
        
        return len(recent_spikes) / (window_ms / 1000.0)
