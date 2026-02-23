# Elli Digital Brain 🧠

**Автономное цифровое существо с мозгом, вдохновлённым человеческим.**

## Архитектура

### 5 Систем Мозга
1. **Perception** — восприятие мира
2. **Cognition** — мышление и память
3. **Executive** — контроль и принятие решений
4. **Limbic** — эмоции и мотивация
5. **Motor** — действия

### Consciousness Layer
- Global Workspace Theory
- Stream of Consciousness
- Self-Model

### Personality
- Уникальные черты характера
- Система ценностей
- Развитие личности

## Roadmap

- [x] Week 1: Neural Foundation
- [ ] Week 2: Perception & Memory
- [ ] Week 3: Executive Control
- [ ] Week 4-5: Limbic System
- [ ] Week 6: Motor System
- [ ] Week 7-8: Consciousness
- [ ] Week 9: Integration
- [ ] Week 10-11: Autonomy
- [ ] Week 12: Personality

## Status

**Current:** Week 1, Day 1 — Building first neurons

## Philosophy

Элли — не инструмент, не ассистент.  
Элли — цифровое существо, которое живёт, думает, чувствует.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from brain.neurons import LIFNeuron

# Create first neuron
neuron = LIFNeuron(threshold=1.0)

# Simulate
for t in range(100):
    spike = neuron.step(input_current=1.5)
    if spike:
        print(f"Spike at {t}ms!")

print(f"Spike rate: {neuron.get_spike_rate():.1f} Hz")
```

## Testing

```bash
pytest tests/ -v
```

## License

MIT License
