# Agentic AI Programming with the Claude Agent SDK

## Pre-Session Setup

### Prerequisites

- Claude Code installed and authenticated (`claude --version` should work)
- Python 3.10+ (`python3 --version`)
- uv package manager (`uv --version` — if not installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Environment setup

```bash
# 1. Confirm Claude Code is authenticated
claude --version

# 2. Confirm no API key override (this would charge API credits instead of your Team sub)
echo $ANTHROPIC_API_KEY
# If it prints a key, run: unset ANTHROPIC_API_KEY

# 3. Create working directory and venv
mkdir -p ~/agentic-training && cd ~/agentic-training
uv venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\activate     # Windows

# 4. Install the SDK
uv pip install claude-agent-sdk
```

### Smoke test

Create `~/agentic-training/smoke_test.py`:

```python
import asyncio
from claude_agent_sdk import query

async def main():
    print("Connecting to Claude Code agent...")
    async for msg in query(prompt="Say hello in one sentence"):
        if hasattr(msg, "result"):
            print(f"Agent responded: {msg.result}")
            print("\n✅ Smoke test passed — you're ready for the session!")

asyncio.run(main())
```

Run it:

```bash
cd ~/agentic-training
python smoke_test.py
```

You should see the agent respond with a greeting and a ✅ message.

### Nuclear reset (if anything goes wrong)

If a dev gets stuck during the session, this gets them back to a clean state:

```bash
cd ~
rm -rf ~/agentic-training
mkdir -p ~/agentic-training && cd ~/agentic-training
uv venv
source .venv/bin/activate
uv pip install claude-agent-sdk
python smoke_test.py
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `CLINotFoundError` | Claude Code CLI not in PATH. Run `which claude` to check. |
| `Authentication error` | Run `claude login`, authenticate with Team account. |
| API charges appearing | `ANTHROPIC_API_KEY` is set. Run `unset ANTHROPIC_API_KEY`. |
| `ModuleNotFoundError: claude_agent_sdk` | Activate venv: `source .venv/bin/activate`, then `uv pip install claude-agent-sdk`. |
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Smoke test hangs | Could be rate limiting on Team plan. Wait a moment, try again. |

---

## 1 — Your First Agent

### Demo

Show the simplest possible agent. Talk through what's happening as it streams.

**File: `01_basic_agent.py`**

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="What files are in the current directory? List them with their sizes.",
        options=ClaudeAgentOptions(
            allowed_tools=["Bash", "Glob", "Read"],
            permission_mode="acceptEdits",
        ),
    ):
        # Show every message type so devs see the agent loop in action
        print(type(message).__name__, "→", getattr(message, "result", str(message)[:200]))

asyncio.run(main())
```

## 2 — Agents That Use Tools

### Demo

Show an agent that does real work — a code reviewer that reads files, runs tests, and produces a report.

**File: `02_code_reviewer.py`**

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

REVIEW_PROMPT = """
Review the Python files in this directory:
1. Read each .py file
2. Run any tests you find (pytest or unittest)
3. Identify bugs, security issues, and style problems
4. Write a REVIEW.md file with your findings, organised by severity

Be thorough but concise.
"""

async def main():
    async for message in query(
        prompt=REVIEW_PROMPT,
        options=ClaudeAgentOptions(
            allowed_tools=["Bash", "Glob", "Read", "Write", "Edit"],
            permission_mode="acceptEdits",
            system_prompt="You are a senior code reviewer. Be direct and specific.",
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

**Before running**, create a deliberately buggy file for it to review:

**File: `buggy_app.py`** (create this before the demo)

```python
import os
import pickle

def load_user_data(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)  # Security: deserialisation vulnerability

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Bug: ZeroDivisionError on empty list

def get_api_key():
    return "sk-1234567890abcdef"  # Security: hardcoded secret

def process_input(user_input):
    result = eval(user_input)  # Security: code injection
    return result

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, name, email):
        self.users[name] = email  # Bug: overwrites if name exists

    def get_user(self, name):
        return self.users[name]  # Bug: KeyError if not found
```

## 3 — Custom Tools via MCP

### Demo

This is the centre piece. Show devs they can give agents access to ANY capability by defining Python functions as tools.

**File: `03_custom_tools.py`**

```python
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
```


**Template for a new tool:**
> ```python
> @tool("my_tool_name", "Description of what it does", {"param1": str, "param2": int})
> async def my_tool_name(args):
>     # Your logic here
>     result = f"Did something with {args['param1']}"
>     return {"content": [{"type": "text", "text": result}]}
> ```
>
> Don't forget to add it to the `tools=[...]` list in `create_sdk_mcp_server()` and
> to `allowed_tools` as `"mcp__internal__my_tool_name"`.


## 4 — Where This Goes

### 4A — Subagents

```python
# Conceptual pattern — a supervisor agent that delegates to specialists

async def run_specialist(task: str, system_prompt: str) -> str:
    """Spawn a focused subagent for a specific job."""
    result_text = ""
    async for msg in query(
        prompt=task,
        options=ClaudeAgentOptions(
            system_prompt=system_prompt,
            allowed_tools=["Read", "Bash", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(msg, "result"):
            result_text = msg.result
    return result_text

# Supervisor orchestrates multiple specialists
security_report = await run_specialist(
    "Audit src/ for security vulnerabilities",
    "You are a security expert. Focus only on security issues."
)

performance_report = await run_specialist(
    "Profile and analyse performance bottlenecks in src/",
    "You are a performance engineer. Focus on speed and memory."
)

# Final synthesis
async for msg in query(
    prompt=f"Combine these reports into a single executive summary:\n\nSecurity:\n{security_report}\n\nPerformance:\n{performance_report}",
    options=ClaudeAgentOptions(allowed_tools=["Write"], permission_mode="acceptEdits"),
):
    pass
```

### 5 — Hooks — Controlling the Agent Loop

```python
# Hooks let you inspect, modify, or block agent actions

options = ClaudeAgentOptions(
    allowed_tools=["Bash", "Read", "Write"],
    permission_mode="acceptEdits",
    hooks={
        # Fires before every tool call — you can approve, modify, or block
        "preToolUse": lambda event: {
            "decision": "block",
            "message": "Bash commands are disabled in this environment"
        } if event.get("tool_name") == "Bash" else {"decision": "approve"},
    },
)
```

### Resources

- Agent SDK docs: `https://platform.claude.com/docs/en/agent-sdk/overview`
- Python SDK reference: `https://platform.claude.com/docs/en/agent-sdk/python`
- GitHub: `https://github.com/anthropics/claude-agent-sdk-python`
- MCP docs: `https://modelcontextprotocol.io`

---

## Appendix: Exercise Files Quick Reference

| File | Block | Purpose |
|------|-------|---------|
| `smoke_test.py` | Pre-session | Verifies SDK + auth works |
| `01_basic_agent.py` | Block 1 | First agent — reads directory |
| `02_code_reviewer.py` | Block 2 | Code reviewer with tools |
| `buggy_app.py` | Block 2 | Deliberately buggy code to review |
| `03_custom_tools.py` | Block 3 | Custom MCP tools |

## Appendix: Troubleshooting

See the troubleshooting table in the Pre-Session Setup section. Additional runtime issues:

| Problem | Solution |
|---------|----------|
| Slow responses | Normal — the agent is doing real work (reading files, running commands). |
| Agent asks for permission | Check `permission_mode="acceptEdits"` is set. |
| Custom tool not found | Check naming: `mcp__<server>__<tool>` in `allowed_tools`. |
