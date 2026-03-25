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