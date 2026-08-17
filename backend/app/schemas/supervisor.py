"""Validated decisions emitted by the multi-agent support supervisor."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator


AgentName = Literal[
    "customer_agent", "billing_agent", "technical_agent", "product_agent",
    "sales_agent", "escalation_agent",
]


class SupervisorDecision(BaseModel):
    """The only control-plane output the supervisor may use to route work."""

    next_agent: AgentName | None = None
    task: str | None = Field(default=None, max_length=1_000)
    reason: str = Field(min_length=1, max_length=1_000)
    status: Literal["continue", "complete"]

    @model_validator(mode="after")
    def validate_route(self) -> "SupervisorDecision":
        if self.status == "continue" and (self.next_agent is None or not self.task):
            raise ValueError("A continuing decision needs next_agent and task.")
        if self.status == "complete" and self.next_agent is not None:
            raise ValueError("A completed decision cannot select an agent.")
        return self


class AgentResult(BaseModel):
    """A specialist outcome the supervisor can safely use for later decisions."""

    status: Literal["completed", "needs_input", "failed"]
    finding: str = Field(min_length=1, max_length=4_000)
    task: str | None = Field(default=None, max_length=1_000)
    evidence: list[dict[str, object]] = Field(default_factory=list)
    error: str | None = Field(default=None, max_length=1_000)
