# Component Scoring Guide

Practical guide for scoring components in the Universal Collapse Scanner framework.

---

## Delta (δ) Component Scoring

### Severity (S)

**For Humanitarian Crises:**

Use `ComponentScoring.severity_humanitarian()`:

```python
severity = ComponentScoring.severity_humanitarian(
    deaths_per_day=150,
    displaced=14_000_000,
    food_insecure=25_000_000
)
```

**Scoring Logic:**

**Deaths per Day:**
- 10,000+: 1.0
- 1,000-9,999: 0.8
- 100-999: 0.6
- 10-99: 0.4
- <10: 0.2

**Displaced (millions):**
- 5M+: 1.0
- 1-5M: 0.8
- 100K-1M: 0.6
- <100K: 0.4

**Food Insecure (millions):**
- 10M+: 1.0
- 5-10M: 0.8
- 1-5M: 0.6
- <1M: 0.4

**Final Score:** Weighted average (40% deaths, 30% displaced, 30% food)

---

### Irreversibility (I)

**Based on Time to Permanent Harm:**

Use `ComponentScoring.irreversibility_days_to_permanent_harm()`:

```python
irreversibility = ComponentScoring.irreversibility_days_to_permanent_harm(days=7)
```

**Scoring:**
- <1 day: 1.0 (immediate permanent harm)
- 1-3 days: 0.8 (acute malnutrition, medical emergencies)
- 4-7 days: 0.6 (health deterioration)
- 8-30 days: 0.4 (chronic harm developing)
- >30 days: 0.2 (long-term processes)

**Examples:**
- Famine (starvation): 7-14 days → 0.6
- Medical supply blockade: 1-3 days → 0.8
- Child development impact: 30+ days → 0.2

---

### Time Pressure (T)

**Based on Deterioration Rate:**

Use `ComponentScoring.time_pressure_rate()`:

```python
time_pressure = ComponentScoring.time_pressure_rate('acute')
```

**Scoring:**
- **Imminent** (1.0): Hours to catastrophe
- **Acute** (0.8): Days to catastrophe
- **Rapid** (0.6): Weeks to catastrophe
- **Gradual** (0.4): Months to catastrophe
- **Chronic** (0.2): Years to catastrophe

**Examples:**
- Active combat zone: Imminent (1.0)
- Blockade with depleting supplies: Acute (0.8)
- Economic sanctions impact: Gradual (0.4)

---

### Response Capacity (R)

**Inverse Scale: Higher value = WORSE δ**

**Manual Scoring (0.0-1.0):**

Consider:
- International access (blocked = high score)
- Local capacity (weak = high score)
- Funding (inadequate = high score)

**Scoring Guide:**
- **0.1-0.3**: Strong international response, full access
- **0.4-0.6**: Moderate response, partial access
- **0.7-0.9**: Weak response, blocked access
- **0.95-1.0**: No response, complete blockade

**Example:**
- UN agencies operating freely: 0.3
- Intermittent access, underfunded: 0.6
- Complete blockade, no aid: 0.9

---

### Recovery Potential (P)

**Inverse Scale: Higher value = WORSE δ**

**Manual Scoring (0.0-1.0):**

Consider:
- Infrastructure damage (extensive = high score)
- Economic base (destroyed = high score)
- Social fabric (fragmented = high score)

**Scoring Guide:**
- **0.1-0.3**: Infrastructure intact, economy functioning
- **0.4-0.6**: Moderate damage, slow recovery possible
- **0.7-0.9**: Extensive damage, generation-long recovery
- **0.95-1.0**: Irreversible destruction

**Example:**
- Economic recession: 0.4
- Post-conflict reconstruction: 0.6
- Genocide aftermath: 0.9

---

## LSSE Component Scoring

### Actual Coverage

**Data Sources:**
- GDELT Project (news database)
- Media Cloud
- Google News search counts
- Academic databases (LexisNexis)

**Methodology:**
1. Define search terms for crisis
2. Count articles in major outlets (30-day window)
3. Weight by outlet reach (optional)

**Example:**
```python
coverage = MediaCoverage(
    actual_articles=1400,  # Counted from GDELT
    expected_articles=12000,  # Estimated from baseline
    timeframe_days=30
)
```

---

### Expected Coverage

**Use Built-in Estimator:**

```python
expected = LSSECalculator.estimate_expected_coverage(
    severity_deaths=50000,
    displacement=5_000_000,
    baseline_crisis='ukraine'
)
```

**Manual Estimation:**

1. Select comparable crisis (similar severity)
2. Measure baseline coverage
3. Scale by severity ratio:
   - Deaths ratio (60% weight)
   - Displacement ratio (40% weight)

**Baseline Examples:**
- Ukraine (2022): ~15,000 articles/month
- Gaza (2023): ~12,000 articles/month
- Syria (peak): ~8,000 articles/month

---

## Psi (Ψ) Component Scoring

### Vulnerability

**Factors:**
- Child/elderly population percentage
- Pre-existing malnutrition rates
- Chronic disease prevalence

**Scoring:**
- High-risk population >50%: 0.8-1.0
- Moderate risk 30-50%: 0.5-0.7
- Low risk <30%: 0.2-0.4

---

### Exposure

**Factors:**
- Geographic exposure (coastal, borders)
- Economic dependence (imports, remittances)
- Climate exposure

**Scoring:**
- Multiple high exposures: 0.8-1.0
- Some exposure: 0.4-0.7
- Limited exposure: 0.1-0.3

---

### Fragility

**Use Fragile States Index:**
- Score 90-120: 0.8-1.0 (critical fragility)
- Score 60-90: 0.5-0.7 (moderate fragility)
- Score <60: 0.2-0.4 (stable)

---

## Gamma (Γ) Component Scoring

### Adaptive Capacity

**Factors:**
- Education levels
- Governance quality
- Technology access

**Scoring:**
- High HDI (>0.8): 0.7-1.0
- Medium HDI (0.5-0.8): 0.4-0.6
- Low HDI (<0.5): 0.1-0.3

---

### Reserves

**Factors:**
- Foreign reserves (months of imports)
- Food stocks
- Medical stockpiles

**Scoring:**
- >6 months reserves: 0.7-1.0
- 3-6 months: 0.4-0.6
- <3 months: 0.1-0.3

---

### Social Cohesion

**Factors:**
- Ethnic/religious fragmentation
- Trust in institutions
- Civil society strength

**Scoring:**
- Low fragmentation, high trust: 0.7-1.0
- Moderate fragmentation: 0.4-0.6
- High fragmentation, low trust: 0.1-0.3

---

## Practical Tips

1. **Start with available data**: Use what you have, estimate where needed
2. **Document assumptions**: Keep notes on scoring rationale
3. **Compare across crises**: Consistency matters more than precision
4. **Update regularly**: Metrics change as situations evolve
5. **Cross-validate**: Check against expert assessments

---

## Example: Complete Scoring

```python
# Humanitarian crisis example
from src.core.delta_calculator import DeltaComponents, ComponentScoring

# Use helper functions
scorer = ComponentScoring()

severity = scorer.severity_humanitarian(
    deaths_per_day=200,      # From ACLED data
    displaced=10_000_000,    # From UNHCR
    food_insecure=20_000_000 # From WFP
)

irreversibility = scorer.irreversibility_days_to_permanent_harm(
    days=5  # Medical assessment
)

time_pressure = scorer.time_pressure_rate('acute')  # Expert judgment

# Manual scoring for response/recovery
components = DeltaComponents(
    severity=severity,
    irreversibility=irreversibility,
    time_pressure=time_pressure,
    response_capacity=0.85,  # Mostly blocked access
    recovery_potential=0.80   # Extensive damage
)
```

---

**Version:** 1.0.0
**Last Updated:** 2025-01-14
