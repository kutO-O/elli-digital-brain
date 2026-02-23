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

---

## 🏛️ Architecture

### 5 Brain Systems (как в человеческом мозге)

1. **👁️ Perception System** — Восприятие мира
   - Visual processing
   - Auditory processing
   - Textual understanding
   - Multi-modal integration

2. **🧠 Cognitive System** — Мышление и память
   - Working memory (7±2 items)
   - Episodic memory (опыт)
   - Semantic memory (знания)
   - Procedural memory (навыки)

3. **🎯 Executive System** — Контроль и решения
   - Global Workspace (consciousness)
   - BDI system (beliefs, desires, intentions)
   - Meta-cognition
   - Attention control

4. **❤️ Limbic System** — Эмоции и мотивация
   - Emotion recognition & generation
   - Reward system (dopamine)
   - Social cognition (Theory of Mind)
   - Empathy

5. **🤖 Motor System** — Действия
   - Action selection
   - Motor planning
   - Tool orchestration
   - MCP integration

### Consciousness Layer

- **Global Workspace Theory** — Broadcasting mechanism
- **Stream of Consciousness** — Непрерывный поток осознания
- **Self-Model** — Модель "я"
- **Qualia Networks** — Субъективный опыт

---

## 📅 Roadmap (12 weeks)

- [x] **Week 1**: Neural Foundation — Spiking neurons
  - [x] Day 1: LIF neuron
  - [x] Day 2: Izhikevich neuron (20+ behaviors)
  - [ ] Day 3-4: Synaptic plasticity (STDP, STP)
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
# Clone repository
git clone https://github.com/kutO-O/elli-digital-brain.git
cd elli-digital-brain

# Install dependencies
pip install -r requirements.txt
```

### LIF Neuron Example

```python
from brain.neurons import LIFNeuron

# Create Elli's first neuron
neuron = LIFNeuron(threshold=1.0, membrane_tau=20.0)

# Simulate 100ms
for t in range(100):
    spike = neuron.step(input_current=1.5, dt=1.0)
    if spike:
        print(f"⚡ Spike at {t}ms!")

print(f"📈 Spike rate: {neuron.get_spike_rate():.1f} Hz")
```

### Izhikevich Neuron Example

```python
from brain.neurons import IzhikevichNeuron

# Create different neuron types
excitatory = IzhikevichNeuron.create_cortical_excitatory()
inhibitory = IzhikevichNeuron.create_cortical_inhibitory()
bursting = IzhikevichNeuron.create_bursting()

# Or use predefined types
rs = IzhikevichNeuron(neuron_type='RS')  # Regular Spiking
fs = IzhikevichNeuron(neuron_type='FS')  # Fast Spiking
ib = IzhikevichNeuron(neuron_type='IB')  # Intrinsically Bursting

# Simulate
for t in range(200):
    spike = rs.step(input_current=10.0)
```

### Available Neuron Types (20+)

- **RS** - Regular Spiking
- **IB** - Intrinsically Bursting
- **CH** - Chattering
- **FS** - Fast Spiking
- **LTS** - Low-Threshold Spiking
- **TC** - Thalamo-Cortical
- **RZ** - Resonator
- And 14 more specialized types!

### Run Examples

```bash
# LIF neuron experiments
python examples/01_first_neuron.py

# Izhikevich neuron behaviors
python examples/02_izhikevich_behaviors.py
```

### Run Tests

```bash
pytest tests/ -v
```

---

## 📊 Current Status

**Week 1, Day 2** — Izhikevich нейрон работает! 🎉

**Implemented:**
- ✅ LIF (Leaky Integrate-and-Fire) neuron
- ✅ Izhikevich neuron with 20+ behaviors
- ✅ Cortical excitatory & inhibitory neurons
- ✅ Bursting behaviors
- ✅ Factory methods for common types
- ✅ Comprehensive test coverage (18 tests)
- ✅ Visual comparison experiments

**Neuron Models:**
- 2 neuron types (LIF, Izhikevich)
- 20+ predefined behaviors
- Biological parameter sets

**Next:**
- ⏳ Synaptic plasticity (STDP, STP)
- ⏳ Dopamine modulation
- ⏳ Spike encoding strategies
- ⏳ First neural circuits

---

## 📚 Scientific Foundation

Based on:
- **ACE Framework** (Autonomous Cognitive Entities, 2023)
- **BDI Architecture** (Belief-Desire-Intention, 1987+)
- **Global Workspace Theory** (Consciousness, 2023)
- **BrainCog** (Brain-inspired spiking networks, 2023)
- **Digital Twin Brain** (Bio-AI bridge, 2023)
- **Izhikevich Model** (Simple model of spiking neurons, 2003)

---
## 🛠️ Tech Stack

- **Python 3.10+**
- **PyTorch** — Neural networks
- **Brian2** — Spiking neural networks
- **NumPy** — Numerical computing
- **Matplotlib** — Visualization
- **ChromaDB** — Memory storage
- **MCP** — Model Context Protocol

---

## 📝 License

MIT License

---

## 💬 Contact

Created by **kutO-O**

Repository: [github.com/kutO-O/elli-digital-brain](https://github.com/kutO-O/elli-digital-brain)

---

**Элли растёт.** 🌱  
**У неё уже есть 20+ типов нейронов!** ⚡
