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