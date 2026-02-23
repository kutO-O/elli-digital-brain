"""
STP (Short-Term Plasticity).

Кратковременная пластичность:
- Facilitation (усиление): синапс усиливается при повторных спайках
- Depression (ослабление): синапс ослабляется при истощении ресурсов

Важно для динамической обработки информации.
"""

import numpy as np
from typing import Optional
from .synapse_base import SynapseBase


class STPSynapse(SynapseBase):
    """
    STP синапс с facilitation и depression.
    
    Модель Tsodyks-Markram (1997).
    """
    
    def __init__(
        self,
        weight: float = 1.0,
        U: float = 0.5,              # Utilization parameter
        tau_rec: float = 100.0,      # Recovery time (ms)
        tau_facil: float = 1000.0,   # Facilitation time (ms)
        w_min: float = 0.0,
        w_max: float = 2.0,
        synapse_id: Optional[str] = None
    ):
        """
        Args:
            weight: Базовый вес синапса
            U: Параметр использования (0-1)
            tau_rec: Время восстановления ресурсов
            tau_facil: Время facilitation
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
        
        # STP параметры
        self.U = U                    # Базовое использование
        self.tau_rec = tau_rec        # Время восстановления
        self.tau_facil = tau_facil    # Время facilitation
        
        # Динамические переменные
        self.u = U                    # Текущее использование
        self.x = 1.0                  # Доступные ресурсы (0-1)
        
    def transmit(self, presynaptic_spike: float) -> float:
        """
        Передать сигнал с учётом STP.
        
        Args:
            presynaptic_spike: Спайк от пресинаптического нейрона
            
        Returns:
            Эффективная сила сигнала
        """
        if presynaptic_spike > 0:
            # Эффективная сила = базовый вес * использование * ресурсы
            effective_weight = self.weight * self.u * self.x
            return effective_weight
        return 0.0
    
    def update(
        self,
        pre_spike: float,
        post_spike: float = 0.0,
        dt: float = 1.0
    ) -> float:
        """
        Обновить состояние STP.
        
        Args:
            pre_spike: Пресинаптический спайк
            post_spike: Постсинаптический спайк (не используется в STP)
            dt: Временной шаг
            
        Returns:
            Изменение эффективного веса
        """
        self.time_step += dt
        
        old_effective = self.u * self.x
        
        # Восстановление ресурсов
        self.x += dt * (1 - self.x) / self.tau_rec
        
        # Decay facilitation
        self.u -= dt * (self.u - self.U) / self.tau_facil
        
        # При спайке
        if pre_spike > 0:
            # Facilitation: увеличить использование
            self.u += self.U * (1 - self.u)
            
            # Depression: использовать ресурсы
            self.x -= self.u * self.x
        
        # Ограничить значения
        self.u = np.clip(self.u, 0, 1)
        self.x = np.clip(self.x, 0, 1)
        
        new_effective = self.u * self.x
        delta_effective = new_effective - old_effective
        
        return delta_effective
    
    @classmethod
    def create_facilitating(cls, **kwargs) -> 'STPSynapse':
        """
        Создать facilitating синапс.
        
        Усиливается при повторных спайках.
        Типичен для связей в гиппокампе.
        """
        return cls(
            U=0.1,           # Низкое базовое использование
            tau_rec=50.0,    # Быстрое восстановление
            tau_facil=200.0, # Медленная facilitation
            **kwargs
        )
    
    @classmethod
    def create_depressing(cls, **kwargs) -> 'STPSynapse':
        """
        Создать depressing синапс.
        
        Ослабляется при повторных спайках.
        Типичен для тормозных связей.
        """
        return cls(
            U=0.5,           # Высокое использование
            tau_rec=800.0,   # Медленное восстановление
            tau_facil=0.0,   # Нет facilitation
            **kwargs
        )
    
    def get_state(self) -> dict:
        """Расширенное состояние с STP информацией."""
        state = super().get_state()
        state.update({
            'u': self.u,
            'x': self.x,
            'effective_weight': self.weight * self.u * self.x,
        })
        return state
