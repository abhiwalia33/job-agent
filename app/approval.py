"""Approval gate: consequential actions are proposed, then run only after explicit approval.

The model never receives an executor. It can only call `propose`. A human (CLI, UI)
calls `approve`, then `execute`. Execution of anything not approved raises.
"""
from collections.abc import Callable

from app.schemas.actions import ActionKind, ProposedAction

Executor = Callable[[ProposedAction], str]


class ApprovalError(Exception):
    pass


class ApprovalGate:
    def __init__(self, executors: dict[ActionKind, Executor] | None = None) -> None:
        self._executors = executors or {}
        self._actions: dict[str, ProposedAction] = {}

    def propose(self, action: ProposedAction) -> ProposedAction:
        self._actions[action.id] = action
        return action

    def pending(self) -> list[ProposedAction]:
        return [a for a in self._actions.values() if a.status == "pending"]

    def approve(self, action_id: str) -> ProposedAction:
        action = self._get(action_id)
        if action.status != "pending":
            raise ApprovalError(f"{action_id} is {action.status}, cannot approve")
        action.status = "approved"
        return action

    def reject(self, action_id: str) -> ProposedAction:
        action = self._get(action_id)
        if action.status != "pending":
            raise ApprovalError(f"{action_id} is {action.status}, cannot reject")
        action.status = "rejected"
        return action

    def execute(self, action_id: str) -> ProposedAction:
        action = self._get(action_id)
        if action.status != "approved":
            raise ApprovalError(f"{action_id} is {action.status}, not approved")
        executor = self._executors.get(action.kind)
        if executor is None:
            raise ApprovalError(f"no executor registered for {action.kind}")
        try:
            action.result = executor(action)
            action.status = "executed"
        except Exception as exc:  # record failure, never retry silently
            action.result = str(exc)
            action.status = "failed"
        return action

    def _get(self, action_id: str) -> ProposedAction:
        try:
            return self._actions[action_id]
        except KeyError:
            raise ApprovalError(f"unknown action {action_id}") from None
