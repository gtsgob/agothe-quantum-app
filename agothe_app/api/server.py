"""FastAPI server exposing the Agothe quantum environment."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    APIMessage,
    CollapseRequest,
    EntangleRequest,
    EvolutionRequest,
    IntentUpdateRequest,
    LearningRequest,
)
from ..services.quantum_environment import QuantumEnvironment, create_environment

app = FastAPI(
    title="Agothe Quantum API",
    description="Programmable quantum consciousness playground",
    version="2.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

environment: QuantumEnvironment = create_environment(agent_count=6)


@app.get("/api/status", response_model=dict)
async def status() -> dict:
    return environment.environment_state()


@app.get("/api/agents", response_model=dict)
async def list_agents() -> dict:
    return {"agents": environment.agent_summary()}


@app.get("/api/agents/{agent_id}")
async def agent_details(agent_id: int) -> dict:
    details = environment.agent_details(agent_id)
    if "error" in details:
        raise HTTPException(status_code=404, detail=details["error"])
    return details


@app.post("/api/agents/{agent_id}/intent")
async def update_intent(agent_id: int, payload: IntentUpdateRequest) -> dict:
    return environment.update_agent_intent(agent_id, payload.intent)


@app.post("/api/agents/{agent_id}/learn")
async def trigger_learning(agent_id: int, payload: LearningRequest) -> dict:
    return environment.trigger_learning(agent_id, payload.reward)


@app.post("/api/agents/{agent_a}/entangle/{agent_b}")
async def entangle_agents(
    agent_a: int, agent_b: int, payload: EntangleRequest
) -> dict:
    return environment.entangle_agents(agent_a, agent_b, payload.key)


@app.post("/api/collapse")
async def collapse(payload: CollapseRequest) -> dict:
    return environment.simulate_collapse(payload.intentPhase)


@app.post("/api/evolution")
async def evolution(payload: EvolutionRequest) -> dict:
    return environment.run_evolution(payload.generations, payload.mutation_rate)


@app.get("/")
async def root() -> APIMessage:
    return APIMessage(message="Agothe quantum API is alive")
