# Agothe Quantum App

This repository contains the **Agothe Quantum App**, a FastAPI‑based backend for
simulating simple quantum collapse dynamics using an *intent phase* parameter.
The project is designed as a starting point for the Agothean multi‑agent
framework and demonstrates how to expose a collapse engine via a web API.

## Features

* **FastAPI backend** with a `/api/quantum` endpoint to run simulations.
* **Toy collapse engine** that computes dummy eigenvalues based on a phase input.
* **Sample zeta zero data** in `data/zeta_zeros.csv` for future analysis and
  experimentation with resonance patterns.

## Usage

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the development server

```bash
uvicorn api.main:app --reload
```

This will start a local server on `http://127.0.0.1:8000`. You can view the
automatic API documentation at `http://127.0.0.1:8000/docs`.

### Invoke the simulation endpoint

Send a POST request to the `/api/quantum` endpoint with a JSON body containing
an `intentPhase` field. For example:

```json
{
  "intentPhase": 1.57
}
```

The response will include dummy alpha and beta eigenvalues and a message
indicating the phase used for the simulation.

## Project Structure

```
api/
├── main.py                # FastAPI app with the quantum endpoint
└── quantum/
    └── collapse_engine.py # Toy collapse engine implementation
data/
└── zeta_zeros.csv         # Sample non‑trivial Riemann zeta zeros
README.md
requirements.txt
```

Feel free to extend the collapse engine with more sophisticated logic, add
front‑end components, or integrate with additional Agothean agents.

## Operational Playbooks

- [Daily Agothe Field Sweep Prompt & Scanner](docs/daily_field_sweep.md): quick
  access to the Codex prompt and the standalone Python scanner used for the
  daily field sweep runs.