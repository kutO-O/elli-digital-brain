"""
Модели нейронов для мозга Элли.
"""

from .neuron_base import NeuronBase
from .lif import LIFNeuron

__all__ = ['NeuronBase', 'LIFNeuron']
