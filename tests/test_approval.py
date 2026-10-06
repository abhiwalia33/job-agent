import pytest

from app.approval import ApprovalError, ApprovalGate
from app.tools.registry import ProposeTool, ReadTool, ToolRegistry


def make():
    sent = []
    gate = ApprovalGate({"save_application": lambda a: sent.append(a.id) or "saved"})
    reg = ToolRegistry(gate)
    reg.add_read(ReadTool("search", "find jobs", lambda q: [q]))
    reg.add_propose(ProposeTool("track", "save application", "save_application"))
    return gate, reg, sent


def test_read_tool_runs_immediately():
    _, reg, _ = make()
    assert reg.call("search", q="ml") == ["ml"]


def test_propose_tool_never_executes():
    gate, reg, sent = make()
    reg.call("track", company="Acme")
    assert sent == []
    assert len(gate.pending()) == 1


def test_cannot_execute_without_approval():
    gate, reg, sent = make()
    reg.call("track", company="Acme")
    aid = gate.pending()[0].id
    with pytest.raises(ApprovalError):
        gate.execute(aid)
    assert sent == []


def test_approve_then_execute():
    gate, reg, sent = make()
    reg.call("track", company="Acme")
    aid = gate.pending()[0].id
    gate.approve(aid)
    assert gate.execute(aid).status == "executed"
    assert sent == [aid]


def test_rejected_cannot_execute_or_reapprove():
    gate, reg, _ = make()
    reg.call("track", company="Acme")
    aid = gate.pending()[0].id
    gate.reject(aid)
    with pytest.raises(ApprovalError):
        gate.execute(aid)
    with pytest.raises(ApprovalError):
        gate.approve(aid)


def test_executed_cannot_run_twice():
    gate, reg, sent = make()
    reg.call("track", company="Acme")
    aid = gate.pending()[0].id
    gate.approve(aid)
    gate.execute(aid)
    with pytest.raises(ApprovalError):
        gate.execute(aid)
    assert len(sent) == 1
