# Universal Collapse Scanner (Tier 1 - Public)

A mathematical framework for measuring system collapse dynamics across humanitarian crises, political systems, and complex domains.

## ⚠️ Ethical Use Notice

This tool is designed for:
- ✅ Crisis analysis and humanitarian advocacy
- ✅ Academic research and methodology validation
- ✅ Policy analysis and transparency work

**NOT for:**
- ❌ Weaponizing information
- ❌ Predictive surveillance of populations
- ❌ Optimizing suppression mechanisms

## Core Concepts

### δ (Delta) - Universal Collapse Coefficient
Measures system destabilization rate:
```
δ = (Severity × Irreversibility × Time_Pressure) / (Response_Capacity × Recovery_Potential)
```

**Thresholds:**
- `δ < 0.35`: Stable
- `δ 0.35-0.65`: Moderate Risk
- `δ 0.65-0.85`: Critical
- `δ > 0.85`: Catastrophic

### LSSE - Large-Scale Suppression Effect
Measures media coverage gaps:
```
LSSE = Actual_Coverage / Expected_Coverage
```

**Thresholds:**
- `LSSE < 0.15`: Extreme suppression
- `LSSE 0.15-0.30`: High suppression
- `LSSE 0.30-0.50`: Moderate suppression
- `LSSE > 0.50`: Adequate coverage

### Millennium Processor
Routes crisis patterns to mathematical constraint geometries for deeper structural analysis.

## Installation

```bash
pip install -r requirements.txt
python setup.py install
```

## Quick Start

```python
from src.core.delta_calculator import DeltaCalculator, DeltaComponents

# Create components
components = DeltaComponents(
    severity=0.85,
    irreversibility=0.75,
    time_pressure=0.90,
    response_capacity=0.80,
    recovery_potential=0.70
)

# Calculate δ
calc = DeltaCalculator()
result = calc.analyze(components)

print(f"δ = {result['delta']} ({result['status']})")
```

## Documentation

- [Methodology](docs/methodology.md) - Full mathematical framework
- [Component Scoring](docs/component_scoring.md) - How to score components
- [Millennium Geometries](docs/millennium_geometries.md) - Constraint geometry routing
- [Ethical Guidelines](docs/ethical_guidelines.md) - Responsible use principles

## Examples

See `examples/` directory for:
- Basic crisis analysis
- LSSE measurement
- Geometry mapping

## License

MIT License - See LICENSE file

## Citation

If you use this framework in research:
```
Universal Collapse Scanner (2025). Agothean Research Framework.
https://github.com/[your-username]/universal-collapse-scanner
```

## Contributing

This is Tier 1 (public educational layer).

For advanced research collaboration, contact [your email].

---

**Remember: With great measurement comes great responsibility.**
