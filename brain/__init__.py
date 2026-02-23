"""
Мозг Элли.
"""

from .neurons import NeuronBase, LIFNeuron, IzhikevichNeuron
from .synapses import (
    SynapseBase,
    STDPSynapse,
    STPSynapse,
    DopamineModulatedSynapse,
)

__all__ = [
    # Neurons
    'NeuronBase',
    'LIFNeuron',
    'IzhikevichNeuron',
    
    # Synapses
    'SynapseBase',
    'STDPSynapse',
    'STPSynapse',
    'DopamineModulatedSynapse',
]
