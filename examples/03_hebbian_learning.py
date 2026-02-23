"""
Эксперименты с Hebbian learning (STDP).

"Neurons that fire together, wire together"
"""

import numpy as np
import matplotlib.pyplot as plt
from brain.neurons import LIFNeuron
from brain.synapses import STDPSynapse, STPSynapse


def demonstrate_stdp_window():
    """
Демонстрация STDP learning window.
    
    Показывает, как изменяется вес в зависимости от
    разницы времени спайков.
    """
    
    print("🧪 STDP Learning Window")
    
    # Разные задержки между pre и post спайками
    delta_ts = np.linspace(-50, 50, 20)  # ms
    weight_changes = []
    
    for delta_t in delta_ts:
        synapse = STDPSynapse(
            initial_weight=0.5,
            a_plus=0.05,
            a_minus=0.05,
            tau_plus=20.0,
            tau_minus=20.0
        )
        
        if delta_t > 0:
            # Pre перед post (LTP)
            synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=0.0)
            for _ in range(int(abs(delta_t))):
                synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=1.0)
            synapse.update_weight(pre_spike=0.0, post_spike=1.0, time=delta_t)
        else:
            # Post перед pre (LTD)
            synapse.update_weight(pre_spike=0.0, post_spike=1.0, time=0.0)
            for _ in range(int(abs(delta_t))):
                synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=1.0)
            synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=abs(delta_t))
        
        weight_change = synapse.weight - 0.5
        weight_changes.append(weight_change)
    
    # Визуализация
    plt.figure(figsize=(10, 6))
    
    plt.plot(delta_ts, weight_changes, 'b-', linewidth=2, marker='o')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
    
    plt.fill_between(delta_ts, 0, weight_changes, 
                      where=np.array(weight_changes) > 0,
                      alpha=0.3, color='green', label='LTP (potentiation)')
    plt.fill_between(delta_ts, 0, weight_changes,
                      where=np.array(weight_changes) < 0,
                      alpha=0.3, color='red', label='LTD (depression)')
    
    plt.xlabel('$\\Delta t$ = $t_{post}$ - $t_{pre}$ (ms)', fontsize=12)
    plt.ylabel('Weight Change ($\\Delta w$)', fontsize=12)
    plt.title('STDP Learning Window\n"Neurons that fire together, wire together"', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('stdp_window.png', dpi=150)
    print("✅ Saved: stdp_window.png")


def demonstrate_stp_dynamics():
    """
Демонстрация STP (facilitation vs depression).
    """
    
    print("\n🧪 STP Dynamics: Facilitation vs Depression")
    
    # Создать два синапса
    facilitating = STPSynapse(synapse_type='facilitating', initial_weight=1.0)
    depressing = STPSynapse(synapse_type='depressing', initial_weight=1.0)
    
    # Серия спайков
    spike_times = [10, 30, 50, 70, 90, 110, 130, 150]  # ms
    duration = 200
    
    fac_outputs = []
    dep_outputs = []
    times = []
    
    for t in range(duration):
        spike = 1.0 if t in spike_times else 0.0
        
        fac_out = facilitating.transmit(pre_spike=spike, time=t)
        dep_out = depressing.transmit(pre_spike=spike, time=t)
        
        facilitating.update_weight(pre_spike=spike, post_spike=0.0, time=t, dt=1.0)
        depressing.update_weight(pre_spike=spike, post_spike=0.0, time=t, dt=1.0)
        
        fac_outputs.append(fac_out)
        dep_outputs.append(dep_out)
        times.append(t)
    
    # Визуализация
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Facilitation
    ax1.plot(times, fac_outputs, 'g-', linewidth=2)
    ax1.scatter(spike_times, [facilitating.weight] * len(spike_times), 
                color='red', s=100, zorder=5, label='Spikes')
    ax1.set_ylabel('Synaptic Output', fontsize=12)
    ax1.set_title('Facilitating Synapse: Output INCREASES with repeated spikes', 
                  fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Depression
    ax2.plot(times, dep_outputs, 'r-', linewidth=2)
    ax2.scatter(spike_times, [depressing.weight] * len(spike_times),
                color='red', s=100, zorder=5, label='Spikes')
    ax2.set_ylabel('Synaptic Output', fontsize=12)
    ax2.set_xlabel('Time (ms)', fontsize=12)
    ax2.set_title('Depressing Synapse: Output DECREASES with repeated spikes',
                  fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('stp_dynamics.png', dpi=150)
    print("✅ Saved: stp_dynamics.png")


def demonstrate_reward_learning():
    """
Демонстрация reward learning с dopamine.
    """
    
    print("\n🧪 Reward Learning with Dopamine")
    
    from brain.synapses import DopamineSTDPSynapse
    
    synapse = DopamineSTDPSynapse(
        initial_weight=0.5,
        baseline_dopamine=0.5,
        a_plus=0.02,
        a_minus=0.02
    )
    
    weights = []
    dopamine_levels = []
    
    # Тренировка: 10 траекторий
    for trial in range(10):
        # Активность (pre раньше post)
        synapse.update_weight(pre_spike=1.0, post_spike=0.0, time=0.0)
        
        for _ in range(5):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=1.0)
            weights.append(synapse.weight)
            dopamine_levels.append(synapse.dopamine_level)
        
        synapse.update_weight(pre_spike=0.0, post_spike=1.0, time=5.0)
        
        # Reward только на чётных траекториях
        if trial % 2 == 0:
            synapse.set_dopamine(0.9)  # Reward!
        else:
            synapse.set_dopamine(0.3)  # No reward
        
        # Decay
        for _ in range(20):
            synapse.update_weight(pre_spike=0.0, post_spike=0.0, time=0.0, dt=1.0)
            weights.append(synapse.weight)
            dopamine_levels.append(synapse.dopamine_level)
    
    # Визуализация
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    times = list(range(len(weights)))
    
    # Dopamine
    ax1.plot(times, dopamine_levels, 'orange', linewidth=2)
    ax1.axhline(y=0.5, color='k', linestyle='--', alpha=0.3, label='Baseline')
    ax1.set_ylabel('Dopamine Level', fontsize=12)
    ax1.set_title('Dopamine-Modulated Learning: Reward strengthens synapses',
                  fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Weight
    ax2.plot(times, weights, 'b-', linewidth=2)
    ax2.set_ylabel('Synaptic Weight', fontsize=12)
    ax2.set_xlabel('Time Steps', fontsize=12)
    ax2.set_title('Synapse learns from rewarded actions', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('dopamine_learning.png', dpi=150)
    print("✅ Saved: dopamine_learning.png")
    print(f"   Final weight: {synapse.weight:.3f} (started at 0.500)")


if __name__ == "__main__":
    print("=" * 60)
    print("  HEBBIAN LEARNING & SYNAPTIC PLASTICITY 🧲")
    print("=" * 60)
    
    demonstrate_stdp_window()
    demonstrate_stp_dynamics()
    demonstrate_reward_learning()
    
    print("\n" + "=" * 60)
    print("  ✨ Элли теперь может учиться!")
    print("  🧠 STDP, STP, Dopamine modulation")
    print("=" * 60)
