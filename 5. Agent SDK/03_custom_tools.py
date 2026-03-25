import asyncio
import json
from datetime import datetime
from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
    ClaudeAgentOptions,
    ClaudeSDKClient,
)

# --- Define custom tools as simple Python functions ---

@tool("get_team_members", "Get the list of team members and their roles", {})
async def get_team_members(args):
    """Simulates calling an internal HR API."""
    team = [
        {"name": "Alice", "role": "Senior Developer", "squad": "Payments"},
        {"name": "Bob", "role": "Junior Developer", "squad": "Payments"},
        {"name": "Charlie", "role": "Tech Lead", "squad": "Platform"},
        {"name": "Diana", "role": "QA Engineer", "squad": "Platform"},
        {"name": "Eve", "role": "DevOps Engineer", "squad": "Infrastructure"},
    ]
    return {"content": [{"type": "text", "text": json.dumps(team, indent=2)}]}


@tool(
    "create_ticket",
    "Create a work item / ticket in the task tracker",
    {"title": str, "description": str, "assignee": str, "priority": str},
)
async def create_ticket(args):
    """Simulates creating a ticket in a project management tool."""
    ticket_id = f"TICK-{datetime.now().strftime('%H%M%S')}"
    ticket = {
        "id": ticket_id,
        "title": args["title"],
        "description": args["description"],
        "assignee": args["assignee"],
        "priority": args["priority"],
        "status": "Created",
    }
    print(f"\n  [TICKET CREATED] {ticket_id}: {args['title']} → {args['assignee']}\n")
    return {"content": [{"type": "text", "text": json.dumps(ticket, indent=2)}]}


@tool(
    "search_codebase",
    "Search the codebase for files matching a pattern or containing specific text",
    {"query": str},
)
async def search_codebase(args):
    """Simulates a code search API (like your RAG system)."""
    # In reality, this would call your RAG MCP or code search API
    results = [
        {"file": "src/payments/processor.py", "match": "class PaymentProcessor", "line": 12},
        {"file": "src/payments/validator.py", "match": "def validate_card", "line": 45},
        {"file": "tests/test_payments.py", "match": "def test_payment_flow", "line": 8},
    ]
    return {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]}


# --- Wire tools into an MCP server and give it to the agent ---

server = create_sdk_mcp_server(
    name="internal-tools",
    version="1.0.0",
    tools=[get_team_members, create_ticket, search_codebase],
)

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"internal": server},
        allowed_tools=[
            "mcp__internal__get_team_members",
            "mcp__internal__create_ticket",
            "mcp__internal__search_codebase",
            "Read",
            "Bash",
        ],
        permission_mode="acceptEdits",
        system_prompt=(
            "You are a development team assistant. You have access to internal tools "
            "for team management, ticket creation, and code search. Use them proactively."
        ),
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(
            "A bug was reported: payments are failing for amounts over R10,000. "
            "Search the codebase for the payment processor, check the team roster "
            "to find the right person to assign it to, and create a high-priority ticket."
        )
        async for msg in client.receive_response():
            if hasattr(msg, "result"):
                print(msg.result)
            elif hasattr(msg, "content"):
                print(str(msg)[:300])

asyncio.run(main())