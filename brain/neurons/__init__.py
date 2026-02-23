"""
Модели нейронов для мозга Элли.
"""

from .neuron_base import NeuronBase
from .lif import LIFNeuron
from .izhikevich import IzhikevichNeuron

__all__ = ['NeuronBase', 'LIFNeuron', 'IzhikevichNeuron']
