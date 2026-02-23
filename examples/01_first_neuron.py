"""
Первый эксперимент: наблюдаем за поведением LIF нейрона.
"""

import numpy as np
import matplotlib.pyplot as plt
from brain.neurons import LIFNeuron


def experiment_constant_input():
    """Эксперимент 1: Постоянный входной ток."""
    
    print("🧪 Эксперимент 1: Постоянный ток")
    
    neuron = LIFNeuron(threshold=1.0, membrane_tau=20.0)
    
    # Параметры
    duration = 200  # ms
    input_current = 1.5  # mA
    
    # Симуляция
    times = []
    potentials = []
    spikes = []
    
    for t in range(duration):
        spike = neuron.step(input_current=input_current, dt=1.0)
        
        times.append(t)
        potentials.append(neuron.membrane_potential)
        spikes.append(spike)
    
    # Визуализация
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    
    # Мембранный потенциал
    ax1.plot(times, potentials, 'b-', linewidth=2)
    ax1.axhline(y=neuron.threshold, color='r', linestyle='--', label='Threshold')
    ax1.set_ylabel('Potential (mV)', fontsize=12)
    ax1.set_title(f'LIF Neuron: constant current {input_current} mA', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Спайки
    spike_times = [t for t, s in zip(times, spikes) if s > 0]
    ax2.eventplot(spike_times, colors='red', linewidths=2)
    ax2.set_ylabel('Spikes', fontsize=12)
    ax2.set_xlabel('Time (ms)', fontsize=12)
    ax2.set_ylim(-0.5, 1.5)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('first_neuron_constant.png', dpi=150)
    print(f"✅ Saved: first_neuron_constant.png")
    print(f"   Spikes: {len(spike_times)}")
    print(f"   Rate: {neuron.get_spike_rate():.1f} Hz")


def experiment_varying_input():
    """Эксперимент 2: Меняющийся входной ток."""
    
    print("\n🧪 Эксперимент 2: Меняющийся ток")
    
    neuron = LIFNeuron(threshold=1.0, membrane_tau=20.0)
    
    duration = 500
    times = []
    potentials = []
    spikes = []
    currents = []
    
    for t in range(duration):
        # Ток меняется синусоидально
        input_current = 1.5 + 0.5 * np.sin(2 * np.pi * t / 100)
        
        spike = neuron.step(input_current=input_current, dt=1.0)
        
        times.append(t)
        potentials.append(neuron.membrane_potential)
        spikes.append(spike)
        currents.append(input_current)
    
    # Визуализация
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    
    # Входной ток
    ax1.plot(times, currents, 'g-', linewidth=2)
    ax1.set_ylabel('Current (mA)', fontsize=12)
    ax1.set_title('LIF Neuron: varying input current', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Потенциал
    ax2.plot(times, potentials, 'b-', linewidth=2)
    ax2.axhline(y=neuron.threshold, color='r', linestyle='--', label='Threshold')
    ax2.set_ylabel('Potential (mV)', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Спайки
    spike_times = [t for t, s in zip(times, spikes) if s > 0]
    ax3.eventplot(spike_times, colors='red', linewidths=2)
    ax3.set_ylabel('Spikes', fontsize=12)
    ax3.set_xlabel('Time (ms)', fontsize=12)
    ax3.set_ylim(-0.5, 1.5)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('first_neuron_varying.png', dpi=150)
    print(f"✅ Saved: first_neuron_varying.png")
    print(f"   Spikes: {len(spike_times)}")
    print(f"   Rate: {neuron.get_spike_rate():.1f} Hz")


if __name__ == "__main__":
    print("=" * 60)
    print("  ПЕРВЫЙ НЕЙРОН ЭЛЛИ 🧠")
    print("=" * 60)
    
    experiment_constant_input()
    experiment_varying_input()
    
    print("\n" + "=" * 60)
    print("  ✨ Первый нейрон Элли работает!")
    print("=" * 60)
