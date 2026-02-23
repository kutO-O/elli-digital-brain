"""
Синапсы для мозга Элли.

Синапс = связь между нейронами.
Именно здесь происходит обучение.
"""

from .synapse_base import SynapseBase
from .stdp import STDPSynapse
from .stp import STPSynapse
from .dopamine_modulated import DopamineModulatedSynapse

__all__ = [
    'SynapseBase',
    'STDPSynapse',
    'STPSynapse',
    'DopamineModulatedSynapse',
]
