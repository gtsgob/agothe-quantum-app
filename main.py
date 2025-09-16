from fastapi import FastAPI, Request
from quantum.collapse_engine import simulate_collapse

# Initialize FastAPI app
app = FastAPI()

# Quantum simulation endpoint
@app.post("/api/quantum")
async def quantum_endpoint(request: Request):
    """
    Endpoint to run a simple quantum collapse simulation.

    Expects a JSON body with an `intentPhase` value (float). If not provided,
    defaults to 0. Returns a JSON object with dummy alpha and beta eigenvalues
    and a message describing the run.
    """
    body = await request.json()
    intent_phase = body.get("intentPhase", 0)
    result = simulate_collapse(intent_phase)
    return result