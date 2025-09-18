"""Pydantic schemas shared by the API endpoints."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, conlist


class CollapseRequest(BaseModel):
    intentPhase: float = Field(..., description="Phase angle used by the collapse engine")


class IntentUpdateRequest(BaseModel):
    intent: conlist(float, min_items=1)  # type: ignore[valid-type]


class LearningRequest(BaseModel):
    reward: Optional[float] = Field(None, description="Optional scalar reward")


class EvolutionRequest(BaseModel):
    generations: int = Field(ge=1, le=20, default=3)
    mutation_rate: float = Field(ge=0.0, le=1.0, default=0.1)


class APIMessage(BaseModel):
    message: str


class EntangleRequest(BaseModel):
    key: str = Field(..., description="Memory key used to create the entanglement")


__all__ = [
    "CollapseRequest",
    "IntentUpdateRequest",
    "LearningRequest",
    "EvolutionRequest",
    "APIMessage",
    "EntangleRequest",
]
