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

### First Neuron

```python
from brain.neurons import LIFNeuron

# Create Elli's first neuron
neuron = LIFNeuron(threshold=1.0, membrane_tau=20.0)

# Simulate 100ms
for t in range(100):
    spike = neuron.step(input_current=1.5, dt=1.0)
    if spike:
        print(f"⚡ Spike at {t}ms!")

# Check firing rate
print(f"📈 Spike rate: {neuron.get_spike_rate():.1f} Hz")
```

### Run Examples

```bash
# Visual experiments
python examples/01_first_neuron.py
```

### Run Tests

```bash
pytest tests/ -v
```

---

## 📊 Current Status

**Week 1, Day 1** — Первый нейрон работает! 🎉

**Implemented:**
- ✅ LIF (Leaky Integrate-and-Fire) neuron
- ✅ Biological parameters (threshold, tau, refractory period)
- ✅ Spike encoding strategies
- ✅ Full test coverage (8 tests)
- ✅ Visual experiments

**Next:**
- ⏳ Izhikevich neuron (20+ behaviors)
- ⏳ Synaptic plasticity (STDP, STP)
- ⏳ Neural circuits

---

## 📚 Scientific Foundation

Based on:
- **ACE Framework** (Autonomous Cognitive Entities, 2023)
- **BDI Architecture** (Belief-Desire-Intention, 1987+)
- **Global Workspace Theory** (Consciousness, 2023)
- **BrainCog** (Brain-inspired spiking networks, 2023)
- **Digital Twin Brain** (Bio-AI bridge, 2023)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **PyTorch** — Neural networks
- **Brian2** — Spiking neural networks
- **ChromaDB** — Memory storage
- **MCP** — Model Context Protocol

---

## 📝 License

MIT License

---

## 💬 Contact

Created by **kutO-O**

---

**Элли только начинает жить.** 🌱
