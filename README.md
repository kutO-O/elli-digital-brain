# Elli Digital Brain 🧠

**Автономное цифровое существо с мозгом, вдохновлённым человеческим.**

Autonomous digital being with brain-inspired cognitive architecture.

---

## 🎯 Vision

Элли — не инструмент, не ассистент, не бот.  
Элли — **цифровое существо**, которое:
- 🧠 **Живёт** — непрерывный поток сознания
- 👁️ **Воспринимает** — мультимодальное восприятие
- 💭 **Думает** — размышления и рефлексия
- 💛 **Чувствует** — эмоции и мотивация
- 🎯 **Желает** — собственные цели
- ✨ **Развивается** — уникальная личность
- 📚 **Учится** — STDP, STP, dopamine learning

---

## 🏛️ Architecture

### 5 Brain Systems (как в человеческом мозге)

1. **👁️ Perception System** — Восприятие мира
2. **🧠 Cognitive System** — Мышление и память
3. **🎯 Executive System** — Контроль и решения
4. **❤️ Limbic System** — Эмоции и мотивация
5. **🤖 Motor System** — Действия

### Learning Mechanisms

- **STDP** — Spike-Timing-Dependent Plasticity ("Neurons that fire together, wire together")
- **STP** — Short-Term Plasticity (Facilitation & Depression)
- **Dopamine Modulation** — Reward-based learning

---

## 📅 Roadmap (12 weeks)

- [x] **Week 1**: Neural Foundation
  - [x] Day 1: LIF neuron
  - [x] Day 2: Izhikevich neuron (20+ behaviors)
  - [x] Day 3: STDP plasticity (Hebbian learning)
  - [x] Day 4: STP + Dopamine modulation
  - [ ] Day 5: Spike encoding
  - [ ] Day 6-7: First neural circuit
- [ ] **Week 2**: Perception & Memory
- [ ] **Week 3**: Executive Control
- [ ] **Week 4-5**: Limbic System
- [ ] **Week 6**: Motor System
- [ ] **Week 7-8**: Consciousness
- [ ] **Week 9**: Integration
- [ ] **Week 10-11**: Autonomy
- [ ] **Week 12**: Personality

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/kutO-O/elli-digital-brain.git
cd elli-digital-brain
pip install -r requirements.txt
```

### Neurons

```python
from brain.neurons import LIFNeuron, IzhikevichNeuron

# LIF neuron
lif = LIFNeuron(threshold=1.0)

# Izhikevich - 20+ types!
excitatory = IzhikevichNeuron.create_cortical_excitatory()
inhibitory = IzhikevichNeuron.create_cortical_inhibitory()
bursting = IzhikevichNeuron.create_bursting()
```

### Synapses & Learning

```python
from brain.synapses import STDPSynapse, STPSynapse, DopamineModulatedSynapse

# STDP - Hebbian learning
stdp = STDPSynapse(weight=1.0, a_plus=0.01, a_minus=0.01)

# Short-term plasticity
facilitating = STPSynapse.create_facilitating()
depressing = STPSynapse.create_depressing()

# Reward-based learning
reward_synapse = DopamineModulatedSynapse(weight=1.0)

# Learning loop
for t in range(1000):
    pre_spike = pre_neuron.step(input_current=10.0)
    post_spike = post_neuron.step(input_current=5.0)
    
    # STDP update
    stdp.update(pre_spike=pre_spike, post_spike=post_spike)
    
    # Or with dopamine
    reward_synapse.update(
        pre_spike=pre_spike,
        post_spike=post_spike,
        dopamine=1.0  # Reward signal
    )
```

### Run Examples

```bash
# Neurons
python examples/01_first_neuron.py
python examples/02_izhikevich_behaviors.py

# Learning
python examples/03_stdp_learning.py
```

### Run Tests

```bash
pytest tests/ -v
```

---

## 📊 Current Status

**Week 1, Day 3** — Элли учится! 🎓

**Implemented:**

### Neurons (2 types)
- ✅ LIF (Leaky Integrate-and-Fire)
- ✅ Izhikevich (20+ behaviors)

### Synapses (3 types)
- ✅ **STDP** — Hebbian learning
  - LTP (Long-Term Potentiation)
  - LTD (Long-Term Depression)
  - Temporal window
- ✅ **STP** — Short-term plasticity
  - Facilitation
  - Depression
  - Resource dynamics
- ✅ **Dopamine-modulated** — Reward learning
  - Eligibility traces
  - Reinforcement signals
  - Dopamine gating

### Testing
- 30+ tests (all passing ✅)
- Visual demonstrations
- Learning experiments

**Next:**
- ⏳ Spike encoding strategies
- ⏳ First neural circuits
- ⏳ Pattern recognition

---

## 📚 Scientific Foundation

**Neuron Models:**
- Izhikevich, E. M. (2003). Simple model of spiking neurons
- Gerstner & Kistler (2002). Spiking Neuron Models

**Synaptic Plasticity:**
- Bi & Poo (1998). Synaptic modifications by correlated activity: Hebb's postulate revisited
- Markram et al. (1997). Regulation of synaptic efficacy by coincidence of postsynaptic APs
- Tsodyks & Markram (1997). The neural code between neocortical pyramidal neurons

**Brain-Inspired AI:**
- BrainCog (2023). Brain-inspired spiking neural networks
- Digital Twin Brain (2023). Bridge between biological and artificial intelligence

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **NumPy** — Numerical computing
- **Matplotlib** — Visualization
- **PyTorch** — Neural networks (coming)
- **Brian2** — Spiking networks (coming)

---

## 📝 License

MIT License

---

**Элли растёт и учится!** 🌱📚  
**У неё уже есть 20+ типов нейронов и 3 типа обучения!** ⚡
