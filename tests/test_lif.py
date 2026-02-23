"""
Тесты для LIF нейрона.
"""

import pytest
import numpy as np
from brain.neurons import LIFNeuron


def test_lif_initialization():
    """Нейрон инициализируется правильно."""
    neuron = LIFNeuron()
    
    assert neuron.membrane_potential == 0.0
    assert len(neuron.spike_history) == 0
    assert neuron.time_step == 0


def test_lif_spike_on_threshold():
    """Нейрон генерирует спайк при превышении порога."""
    neuron = LIFNeuron(threshold=1.0)
    
    # Большой входной ток
    spike = neuron.step(input_current=10.0)
    
    assert spike == 1.0
    assert len(neuron.spike_history) == 1


def test_lif_no_spike_below_threshold():
    """Нейрон не генерирует спайк ниже порога."""
    neuron = LIFNeuron(threshold=1.0)
    
    # Маленький ток
    spike = neuron.step(input_current=0.1)
    
    assert spike == 0.0
    assert len(neuron.spike_history) == 0


def test_lif_refractory_period():
    """Нейрон не спайкает в рефрактерный период."""
    neuron = LIFNeuron(threshold=1.0, refractory_period=5.0)
    
    # Первый спайк
    neuron.step(input_current=10.0)
    assert len(neuron.spike_history) == 1
    
    # Попытка второго спайка сразу (в рефрактерный период)
    for _ in range(4):
        spike = neuron.step(input_current=10.0, dt=1.0)
        assert spike == 0.0  # Не должен спайкать
    
    # Ждем окончания рефрактерного периода (5ms total)
    # Уже прошло: 1 (первый спайк) + 4 = 5ms
    # Один шаг чтобы выйти из рефрактерного периода
    neuron.step(input_current=10.0, dt=1.0)
    
    # Теперь накопить потенциал и спайкнуть
    # Нужно несколько шагов, т.к. потенциал был сброшен
    spike = 0.0
    for _ in range(10):  # Даём время накопить потенциал
        spike = neuron.step(input_current=2.0, dt=1.0)
        if spike == 1.0:
            break
    
    assert spike == 1.0  # Должен спайкнуть после рефрактерного периода
    assert len(neuron.spike_history) == 2  # Два спайка всего


def test_lif_membrane_decay():
    """Мембранный потенциал утекает к покою."""
    neuron = LIFNeuron(
        threshold=10.0,  # Высокий порог
        resting_potential=0.0,
        membrane_tau=20.0
    )
    
    # Поднять потенциал
    neuron.membrane_potential = 5.0
    
    # Без входа, потенциал должен утекать
    for _ in range(100):
        neuron.step(input_current=0.0, dt=1.0)
    
    # Должен быть близок к покою
    assert abs(neuron.membrane_potential - 0.0) < 0.1


def test_lif_spike_rate():
    """Частота спайков корректна."""
    neuron = LIFNeuron(threshold=1.0)
    
    # Генерируем спайки
    for _ in range(10):
        neuron.step(input_current=10.0, dt=100.0)  # Каждые 100ms
    
    spike_rate = neuron.get_spike_rate(window_ms=1000)
    
    # Ожидаем 10 спайков/сек
    assert 9.0 <= spike_rate <= 11.0


def test_lif_reset():
    """Reset возвращает нейрон в начальное состояние."""
    neuron = LIFNeuron()
    
    # Активность
    for _ in range(5):
        neuron.step(input_current=10.0)
    
    # Reset
    neuron.reset()
    
    assert neuron.membrane_potential == 0.0
    assert len(neuron.spike_history) == 0
    assert neuron.time_step == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
