import asyncio
from claude_agent_sdk import query

async def main():
    print("Connecting to Claude Code agent...")
    async for msg in query(prompt="Say hello in one sentence"):
        if hasattr(msg, "result"):
            print(f"Agent responded: {msg.result}")
            print("\n✅ Smoke test passed — you're ready for the session!")

asyncio.run(main())