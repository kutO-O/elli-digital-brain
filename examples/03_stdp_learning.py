"""
Эксперименты с STDP синапсом.

Показываем Hebbian learning: "neurons that fire together, wire together".
"""

import numpy as np
import matplotlib.pyplot as plt
from brain.neurons import LIFNeuron
from brain.synapses import STDPSynapse


def visualize_stdp_window():
    """Визуализировать STDP окно."""
    
    print("🧪 STDP Learning Window")
    
    synapse = STDPSynapse(a_plus=0.01, a_minus=0.01, tau_plus=20.0, tau_minus=20.0)
    
    window = synapse.get_stdp_window(delta_t_range=(-100, 100))
    
    plt.figure(figsize=(10, 6))
    plt.plot(window['delta_t'], window['delta_w'], 'b-', linewidth=3)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
    
    plt.xlabel('$\Delta t$ (post - pre) [ms]', fontsize=14)
    plt.ylabel('$\Delta w$ (weight change)', fontsize=14)
    plt.title('STDP Learning Window\n"Neurons that fire together, wire together"', 
              fontsize=16, fontweight='bold')
    
    # Аннотации
    plt.text(30, 0.005, 'LTP\n(potentiation)', fontsize=12, ha='center', 
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    plt.text(-30, -0.005, 'LTD\n(depression)', fontsize=12, ha='center',
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('stdp_window.png', dpi=150)
    print("✅ Saved: stdp_window.png")


def demonstrate_hebbian_learning():
    """Демонстрация Hebbian learning."""
    
    print("\n🧪 Hebbian Learning Demo")
    
    # 2 нейрона + STDP синапс
    pre_neuron = LIFNeuron(threshold=1.0)
    post_neuron = LIFNeuron(threshold=1.0)
    synapse = STDPSynapse(weight=0.5, a_plus=0.05, a_minus=0.05)
    
    duration = 1000
    input_to_pre = 2.0
    input_to_post = 0.5  # Недостаточно для спайка
    
    times = []
    weights = []
    pre_spikes = []
    post_spikes = []
    
    for t in range(duration):
        # Пресинаптический нейрон
        pre_spike = pre_neuron.step(input_current=input_to_pre)
        
        # Синаптическая передача
        synaptic_input = synapse.transmit(pre_spike)
        
        # Постсинаптический нейрон
        post_spike = post_neuron.step(input_current=input_to_post + synaptic_input)
        
        # STDP обновление
        synapse.update(pre_spike=pre_spike, post_spike=post_spike)
        
        times.append(t)
        weights.append(synapse.weight)
        pre_spikes.append(pre_spike)
        post_spikes.append(post_spike)
    
    # Визуализация
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    
    # Вес синапса
    ax1.plot(times, weights, 'b-', linewidth=2)
    ax1.set_ylabel('Synaptic Weight', fontsize=12)
    ax1.set_title('Hebbian Learning: Weight increases when neurons fire together', 
                  fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Pre спайки
    pre_times = [t for t, s in zip(times, pre_spikes) if s > 0]
    ax2.eventplot(pre_times, colors='red', linewidths=2)
    ax2.set_ylabel('Pre Neuron', fontsize=12)
    ax2.set_ylim(-0.5, 1.5)
    ax2.grid(True, alpha=0.3)
    
    # Post спайки
    post_times = [t for t, s in zip(times, post_spikes) if s > 0]
    ax3.eventplot(post_times, colors='blue', linewidths=2)
    ax3.set_ylabel('Post Neuron', fontsize=12)
    ax3.set_xlabel('Time (ms)', fontsize=12)
    ax3.set_ylim(-0.5, 1.5)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('hebbian_learning.png', dpi=150)
    print("✅ Saved: hebbian_learning.png")
    print(f"   Initial weight: 0.5")
    print(f"   Final weight: {weights[-1]:.3f}")
    print(f"   Pre spikes: {len(pre_times)}")
    print(f"   Post spikes: {len(post_times)}")


def compare_stdp_timings():
    """Сравнение разных временных задержек."""
    
    print("\n🧪 STDP Timing Comparison")
    
    delays = [-20, -10, 0, 10, 20]  # ms
    final_weights = []
    
    for delay in delays:
        synapse = STDPSynapse(weight=1.0, a_plus=0.1, a_minus=0.1)
        
        # 100 пар спайков
        for _ in range(100):
            if delay < 0:
                # Post перед pre
                synapse.update(pre_spike=0.0, post_spike=1.0)
                for _ in range(abs(delay)):
                    synapse.update(pre_spike=0.0, post_spike=0.0)
                synapse.update(pre_spike=1.0, post_spike=0.0)
            else:
                # Pre перед post
                synapse.update(pre_spike=1.0, post_spike=0.0)
                for _ in range(abs(delay)):
                    synapse.update(pre_spike=0.0, post_spike=0.0)
                synapse.update(pre_spike=0.0, post_spike=1.0)
            
            # Пауза
            for _ in range(50):
                synapse.update(pre_spike=0.0, post_spike=0.0)
        
        final_weights.append(synapse.weight)
    
    # Визуализация
    plt.figure(figsize=(10, 6))
    colors = ['red' if d < 0 else 'green' for d in delays]
    plt.bar(delays, final_weights, color=colors, alpha=0.7, width=5)
    plt.axhline(y=1.0, color='k', linestyle='--', label='Initial weight')
    plt.xlabel('Spike timing delay (ms)', fontsize=14)
    plt.ylabel('Final weight', fontsize=14)
    plt.title('STDP: Weight change depends on spike timing', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('stdp_timing_comparison.png', dpi=150)
    print("✅ Saved: stdp_timing_comparison.png")


if __name__ == "__main__":
    print("=" * 60)
    print("  STDP - HEBBIAN LEARNING 🧠")
    print("=" * 60)
    
    visualize_stdp_window()
    demonstrate_hebbian_learning()
    compare_stdp_timings()
    
    print("\n" + "=" * 60)
    print("  ✨ STDP работает! Элли учится!")
    print("=" * 60)
