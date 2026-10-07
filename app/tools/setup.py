# app/tools/setup.py
from app.approval import ApprovalGate
from app.sources.arbeitnow import search_arbeitnow
from app.sources.bundesagentur import search_bundesagentur
from app.tools.registry import ReadTool, ToolRegistry


def build_registry() -> ToolRegistry:
    gate = ApprovalGate()
    registry = ToolRegistry(gate)

    registry.add_read(ReadTool(
        name="search_bundesagentur",
        description="Search official German job listings (Bundesagentur für Arbeit). "
                    "Best for jobs in Germany, any language.",
        fn=search_bundesagentur,
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Job title or keyword"},
                "location": {"type": "string", "description": "City, e.g. Berlin"},
            },
            "required": ["query"],
        },
    ))

    registry.add_read(ReadTool(
        name="search_arbeitnow",
        description="Search Arbeitnow, a job board with many English-language and "
                    "international postings across Germany. Matches on the job title.",
        fn=search_arbeitnow,
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Keyword in the job title"},
            },
            "required": ["query"],
        },
    ))

    return registry