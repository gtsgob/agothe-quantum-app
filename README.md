# Agothe Quantum App

The Agothe Quantum App is a fully featured playground for experimenting with the
fictional Agothe quantum consciousness framework.  The project now bundles a
rich Streamlit dashboard, a programmable FastAPI backend and a reusable Python
package for orchestrating synthetic "quantum" agents.

## Highlights

- **Quantum agent package** – reusable classes describing intent vectors,
  entangled memories and collapse behaviour (`agothe_app.core`).
- **Evolutionary protocol** – a Darwin-inspired routine that mutates and
  evolves populations of agents over multiple generations.
- **Service layer** – a `QuantumEnvironment` orchestrator powering the CLI,
  API and the front-end experience.
- **Interactive dashboard** – explore agents, visualise quantum state
  probabilities and trigger collapse simulations directly from Streamlit.
- **FastAPI backend** – REST endpoints for listing agents, updating intent,
  invoking the collapse engine and running evolution experiments.

## Getting started

### Installation

```bash
pip install -r requirements.txt
```

### Command line demo

```bash
python main.py --demo --agents 6
```

### Launch the Streamlit interface

```bash
python main.py --web
```

### Run the FastAPI server

```bash
uvicorn agothe_app.api.server:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.  The most
useful endpoints are:

- `GET /api/status` – high level environment overview.
- `GET /api/agents` – list agents with coherence metrics.
- `POST /api/agents/{id}/intent` – update an agent intent vector.
- `POST /api/collapse` – execute the toy collapse engine.
- `POST /api/evolution` – run several generations of the evolutionary protocol.

## Repository structure

```
agothe_app/
├── api/                   # FastAPI application
├── core/                  # Quantum agent primitives and evolution logic
├── navigation/            # Navigation helpers for the dashboard
└── services/              # Quantum environment orchestrator
main.py                    # CLI entry point
streamlit_app.py           # Streamlit dashboard
requirements.txt           # Python dependencies
```

## Development

The project was designed to be easily extensible.  The `QuantumEnvironment`
class exposes a clean API that can be reused by new interfaces.  Pull requests
are welcome – try wiring the agents to real ML models or extend the collapse
engine with richer physics!
