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
* **Field scanner daily sweep toolkit** in `field_scanner/` for orchestrating
  daily scanning routines and generating structured sweep reports.

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

### Run the field scanner daily sweep demo

A minimal CLI is available for generating a synthetic daily sweep report. Supply
any JSON configuration following the shape of
`field_scanner/sample_config.json`:

```bash
python -m field_scanner.cli field_scanner/sample_config.json --export sweep.json
```

The command prints a concise summary to stdout and, when `--export` is
specified, writes a detailed JSON snapshot for downstream automation.

## Project Structure

```
api/
├── main.py                # FastAPI app with the quantum endpoint
└── quantum/
    └── collapse_engine.py # Toy collapse engine implementation
field_scanner/
├── __init__.py            # Exposes the daily sweep API
├── cli.py                 # Command line interface for the sweep
├── daily_sweep.py         # Sweep orchestration logic
├── data_models.py         # Data models and helpers
└── sample_config.json     # Example configuration
data/
└── zeta_zeros.csv         # Sample non‑trivial Riemann zeta zeros
README.md
requirements.txt
```

Feel free to extend the collapse engine with more sophisticated logic, add
front‑end components, or integrate with additional Agothean agents.
