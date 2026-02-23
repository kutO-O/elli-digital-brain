"""
Синапсы для мозга Элли.
"""

from .synapse_base import SynapseBase
from .stdp import STDPSynapse
from .stp import STPSynapse
from .dopamine_stdp import DopamineSTDPSynapse

__all__ = [
    'SynapseBase',
    'STDPSynapse',
    'STPSynapse',
    'DopamineSTDPSynapse',
]
