"""
Тесты для Izhikevich нейрона.
"""

import pytest
import numpy as np
from brain.neurons import IzhikevichNeuron


def test_izhikevich_initialization():
    """Нейрон инициализируется с параметрами по умолчанию."""
    neuron = IzhikevichNeuron()
    
    assert neuron.a == 0.02
    assert neuron.b == 0.2
    assert neuron.c == -65.0
    assert neuron.d == 8.0
    assert neuron.v == -65.0
    assert len(neuron.spike_history) == 0


def test_izhikevich_predefined_types():
    """Предопределённые типы нейронов создаются правильно."""
    
    # Regular Spiking
    rs = IzhikevichNeuron(neuron_type='RS')
    assert rs.type_name == 'Regular Spiking'
    assert rs.a == 0.02
    
    # Fast Spiking
    fs = IzhikevichNeuron(neuron_type='FS')
    assert fs.type_name == 'Fast Spiking'
    assert fs.a == 0.1
    
    # Intrinsically Bursting
    ib = IzhikevichNeuron(neuron_type='IB')
    assert ib.type_name == 'Intrinsically Bursting'
    assert ib.c == -55


def test_izhikevich_invalid_type():
    """Неправильный тип вызывает ошибку."""
    with pytest.raises(ValueError):
        IzhikevichNeuron(neuron_type='INVALID_TYPE')


def test_izhikevich_spike_generation():
    """Нейрон генерирует спайки."""
    neuron = IzhikevichNeuron(neuron_type='RS')
    
    # Симулируем с постоянным током
    spikes = []
    for _ in range(200):
        spike = neuron.step(input_current=10.0, dt=1.0)
        spikes.append(spike)
    
    # Должны быть спайки
    assert sum(spikes) > 0
    assert len(neuron.spike_history) > 0


def test_izhikevich_fs_faster_than_rs():
    """
Fast Spiking нейроны спайкают чаще Regular Spiking."""
    
    rs = IzhikevichNeuron(neuron_type='RS')
    fs = IzhikevichNeuron(neuron_type='FS')
    
    # Одинаковый входной ток
    input_current = 10.0
    
    for _ in range(200):
        rs.step(input_current=input_current, dt=1.0)
        fs.step(input_current=input_current, dt=1.0)
    
    # FS должен спайкать чаще
    assert len(fs.spike_history) > len(rs.spike_history)


def test_izhikevich_bursting():
    """
Intrinsically Bursting нейрон генерирует группы спайков."""
    
    ib = IzhikevichNeuron(neuron_type='IB')
    
    # Симулируем
    spikes = []
    for t in range(200):
        spike = ib.step(input_current=10.0, dt=1.0)
        spikes.append((t, spike))
    
    # Проверяем наличие burst (группы спайков)
    spike_times = [t for t, s in spikes if s > 0]
    
    if len(spike_times) >= 2:
        # Проверяем inter-spike intervals
        isi = np.diff(spike_times)
        
        # Bursting: некоторые ISI должны быть очень маленькими
        assert np.min(isi) < 10  # Быстрые спайки в burst


def test_izhikevich_factory_methods():
    """
Factory methods создают правильные нейроны."""
    
    excitatory = IzhikevichNeuron.create_cortical_excitatory()
    assert excitatory.type_name == 'Regular Spiking'
    
    inhibitory = IzhikevichNeuron.create_cortical_inhibitory()
    assert inhibitory.type_name == 'Fast Spiking'
    
    bursting = IzhikevichNeuron.create_bursting()
    assert bursting.type_name == 'Intrinsically Bursting'


def test_izhikevich_get_state():
    """
get_state() возвращает полное состояние."""
    neuron = IzhikevichNeuron(neuron_type='RS')
    
    # Немного симуляции
    for _ in range(50):
        neuron.step(input_current=10.0)
    
    state = neuron.get_state()
    
    assert 'neuron_id' in state
    assert 'type' in state
    assert state['type'] == 'Regular Spiking'
    assert 'v' in state
    assert 'u' in state
    assert 'spike_count' in state
    assert 'parameters' in state
    assert state['parameters']['a'] == 0.02


def test_izhikevich_reset():
    """reset() возвращает нейрон в начальное состояние."""
    neuron = IzhikevichNeuron()
    
    # Активность
    for _ in range(50):
        neuron.step(input_current=10.0)
    
    # Reset
    neuron.reset()
    
    assert len(neuron.spike_history) == 0
    assert neuron.time_step == 0


def test_izhikevich_all_neuron_types():
    """Все предопределённые типы создаются без ошибок."""
    
    for neuron_type in IzhikevichNeuron.NEURON_TYPES.keys():
        neuron = IzhikevichNeuron(neuron_type=neuron_type)
        
        # Проверяем, что может симулироваться
        for _ in range(10):
            neuron.step(input_current=10.0)
        
        # Не должно быть ошибок
        assert neuron is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
