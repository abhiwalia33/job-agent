"""Tool registry. Read-only tools run immediately; consequential tools only create proposals."""
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.approval import ApprovalGate
from app.schemas.actions import ActionKind, ProposedAction


@dataclass
class ReadTool:
    name: str
    description: str
    fn: Callable[..., Any]


@dataclass
class ProposeTool:
    name: str
    description: str
    kind: ActionKind


class ToolRegistry:
    def __init__(self, gate: ApprovalGate) -> None:
        self._gate = gate
        self._read: dict[str, ReadTool] = {}
        self._propose: dict[str, ProposeTool] = {}

    def add_read(self, tool: ReadTool) -> None:
        self._read[tool.name] = tool

    def add_propose(self, tool: ProposeTool) -> None:
        self._propose[tool.name] = tool

    def call(self, name: str, **kwargs: Any) -> Any:
        """Entry point for the agent loop. Never executes a consequential action."""
        if name in self._read:
            return self._read[name].fn(**kwargs)
        if name in self._propose:
            tool = self._propose[name]
            summary = kwargs.pop("summary", tool.description)
            action = ProposedAction(kind=tool.kind, summary=summary, payload=kwargs)
            self._gate.propose(action)
            return f"Proposed {action.id}: {action.summary}. Waiting for user approval."
        raise KeyError(f"unknown tool {name}")
