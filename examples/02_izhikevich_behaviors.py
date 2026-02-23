"""
Эксперименты с Izhikevich нейроном.

Показываем различные типы поведения нейронов.
"""

import numpy as np
import matplotlib.pyplot as plt
from brain.neurons import IzhikevichNeuron


def compare_neuron_types():
    """Сравнение разных типов нейронов."""
    
    print("🧪 Сравнение 6 типов нейронов")
    
    # Создаём 6 разных типов
    neuron_types = ['RS', 'IB', 'CH', 'FS', 'LTS', 'RZ']
    neurons = {ntype: IzhikevichNeuron(neuron_type=ntype) for ntype in neuron_types}
    
    # Параметры симуляции
    duration = 200  # ms
    input_current = 10.0  # pA
    
    # Симуляция
    data = {ntype: {'times': [], 'v': [], 'spikes': []} for ntype in neuron_types}
    
    for t in range(duration):
        for ntype in neuron_types:
            spike = neurons[ntype].step(input_current=input_current, dt=1.0)
            
            data[ntype]['times'].append(t)
            data[ntype]['v'].append(neurons[ntype].v)
            data[ntype]['spikes'].append(spike)
    
    # Визуализация
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, ntype in enumerate(neuron_types):
        ax = axes[idx]
        neuron = neurons[ntype]
        
        # Потенциал
        ax.plot(data[ntype]['times'], data[ntype]['v'], 'b-', linewidth=1.5)
        ax.axhline(y=30, color='r', linestyle='--', alpha=0.5, label='Spike threshold')
        
        # Заголовок
        spike_count = len(neuron.spike_history)
        ax.set_title(
            f"{neuron.type_name} ({ntype})\n"
            f"Spikes: {spike_count}, Rate: {neuron.get_spike_rate():.1f} Hz",
            fontsize=10, fontweight='bold'
        )
        
        ax.set_ylabel('v (mV)', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        if idx >= 4:
            ax.set_xlabel('Time (ms)', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('izhikevich_comparison.png', dpi=150)
    print("✅ Saved: izhikevich_comparison.png")
    
    # Статистика
    print("\nСтатистика:")
    for ntype in neuron_types:
        neuron = neurons[ntype]
        print(f"  {neuron.type_name:30s}: {len(neuron.spike_history):3d} spikes ({neuron.get_spike_rate():.1f} Hz)")


def demonstrate_bursting():
    """Демонстрация bursting поведения."""
    
    print("\n🧪 Bursting поведение")
    
    # Intrinsically Bursting нейрон
    ib = IzhikevichNeuron(neuron_type='IB')
    
    duration = 300
    input_current = 10.0
    
    times = []
    voltages = []
    recovery = []
    spikes = []
    
    for t in range(duration):
        spike = ib.step(input_current=input_current, dt=1.0)
        
        times.append(t)
        voltages.append(ib.v)
        recovery.append(ib.u)
        spikes.append(spike)
    
    # Визуализация
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    
    # Мембранный потенциал
    ax1.plot(times, voltages, 'b-', linewidth=2)
    ax1.axhline(y=30, color='r', linestyle='--', alpha=0.5, label='Threshold')
    ax1.set_ylabel('Membrane Potential v (mV)', fontsize=12)
    ax1.set_title('Intrinsically Bursting Neuron - Burst Behavior', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Восстановительная переменная
    ax2.plot(times, recovery, 'g-', linewidth=2)
    ax2.set_ylabel('Recovery Variable u', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Спайки
    spike_times = [t for t, s in zip(times, spikes) if s > 0]
    ax3.eventplot(spike_times, colors='red', linewidths=2)
    ax3.set_ylabel('Spikes', fontsize=12)
    ax3.set_xlabel('Time (ms)', fontsize=12)
    ax3.set_ylim(-0.5, 1.5)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('izhikevich_bursting.png', dpi=150)
    print("✅ Saved: izhikevich_bursting.png")
    print(f"   Total spikes: {len(spike_times)}")
    print(f"   Spike rate: {ib.get_spike_rate():.1f} Hz")
    
    # Анализ burst patterns
    if len(spike_times) >= 2:
        isi = np.diff(spike_times)
        print(f"   ISI range: {np.min(isi):.1f} - {np.max(isi):.1f} ms")
        print(f"   Mean ISI: {np.mean(isi):.1f} ms")


def compare_lif_vs_izhikevich():
    """Сравнение LIF и Izhikevich."""
    
    print("\n🧪 Сравнение LIF vs Izhikevich")
    
    from brain.neurons import LIFNeuron
    
    lif = LIFNeuron(threshold=1.0, membrane_tau=20.0)
    izh = IzhikevichNeuron(neuron_type='RS')
    
    duration = 200
    input_current_lif = 1.5  # mA
    input_current_izh = 10.0  # pA
    
    lif_data = {'times': [], 'v': [], 'spikes': []}
    izh_data = {'times': [], 'v': [], 'spikes': []}
    
    for t in range(duration):
        lif_spike = lif.step(input_current=input_current_lif, dt=1.0)
        izh_spike = izh.step(input_current=input_current_izh, dt=1.0)
        
        lif_data['times'].append(t)
        lif_data['v'].append(lif.membrane_potential)
        lif_data['spikes'].append(lif_spike)
        
        izh_data['times'].append(t)
        izh_data['v'].append(izh.v)
        izh_data['spikes'].append(izh_spike)
    
    # Визуализация
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # LIF
    ax1.plot(lif_data['times'], lif_data['v'], 'b-', linewidth=2, label='LIF')
    ax1.axhline(y=lif.threshold, color='r', linestyle='--', alpha=0.5)
    ax1.set_ylabel('LIF Potential (mV)', fontsize=12)
    ax1.set_title(f'LIF Neuron: {len(lif.spike_history)} spikes, {lif.get_spike_rate():.1f} Hz', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Izhikevich
    ax2.plot(izh_data['times'], izh_data['v'], 'g-', linewidth=2, label='Izhikevich RS')
    ax2.axhline(y=30, color='r', linestyle='--', alpha=0.5)
    ax2.set_ylabel('Izhikevich Potential (mV)', fontsize=12)
    ax2.set_xlabel('Time (ms)', fontsize=12)
    ax2.set_title(f'Izhikevich RS: {len(izh.spike_history)} spikes, {izh.get_spike_rate():.1f} Hz', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('lif_vs_izhikevich.png', dpi=150)
    print("✅ Saved: lif_vs_izhikevich.png")


if __name__ == "__main__":
    print("=" * 60)
    print("  IZHIKEVICH NEURON - 20+ ПОВЕДЕНИЙ 🧠")
    print("=" * 60)
    
    compare_neuron_types()
    demonstrate_bursting()
    compare_lif_vs_izhikevich()
    
    print("\n" + "=" * 60)
    print("  ✨ Izhikevich нейрон работает!")
    print("  Элли теперь имеет 20+ типов нейронов!")
    print("=" * 60)
