"""Main LangGraph workflow for the DevOps AI agent."""

from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from src.agent.config import AgentConfig, load_config
from src.agent.prompts import get_pr_review_system_prompt
from src.agent.state import AgentState
from src.tools.pr_review.analyze_code import analyze_code
from src.tools.pr_review.check_appconfig_key import check_appconfig_key
from src.tools.pr_review.comment import format_review_comments
from src.utils.logging import get_logger

logger = get_logger("agent.graph")

# Default tools available to the agent during review.
# fetch_pr_details is NOT included — the skill pre-fetches all PR data
# before invoking the graph, so the LLM never needs to call it.
REVIEW_TOOLS = [
    analyze_code,
    format_review_comments,
    check_appconfig_key,
]


def _build_system_message(state: AgentState, system_prompt: str | None = None) -> SystemMessage:
    """Build the system message with context for prompt caching."""
    prompt = system_prompt or get_pr_review_system_prompt()

    # Add PR context if available
    if state.pr_context.pull_request_id:
        ctx = state.pr_context
        prompt += f"""

## Current PR Context
- **Title:** {ctx.title}
- **Author:** {ctx.author}
- **Source Branch:** {ctx.source_branch}
- **Target Branch:** {ctx.target_branch}
- **Changed Files ({len(ctx.changed_files)}):** {', '.join(ctx.changed_files[:20])}
"""
        if ctx.description:
            prompt += f"\n**Description:**\n{ctx.description}\n"

    return SystemMessage(content=prompt)


# --- Graph nodes ---


def _make_reasoning_node(tools: list, system_prompt: str | None = None, config: AgentConfig | None = None):
    """Create a reasoning node bound to a specific tool set."""

    config = config or load_config()
    model = ChatAnthropic(
        model=config.model_name,
        api_key=config.anthropic_api_key,
        max_tokens=config.max_tokens,
        temperature=config.temperature,
    ).bind_tools(tools)

    def reasoning_node(state: AgentState) -> dict:
        """Main reasoning node: the LLM decides what to do next."""
        logger.info("reasoning_node", step=state.current_step, retry=state.retry_count)

        system_msg = _build_system_message(state, system_prompt)
        messages = [system_msg] + list(state.messages)

        try:
            response = model.invoke(messages)
            return {"messages": [response], "current_step": "reasoning"}
        except Exception as e:
            logger.error("reasoning_error", error=str(e))
            if state.retry_count < state.max_retries:
                return {
                    "retry_count": state.retry_count + 1,
                    "error": str(e),
                    "current_step": "reasoning",
                }
            return {"error": str(e), "current_step": "error"}

    return reasoning_node


def should_continue(state: AgentState) -> str:
    """Route after reasoning: continue with tools or finish."""
    if state.error and state.retry_count >= state.max_retries:
        return "error"

    # Check if the last message has tool calls
    if state.messages:
        last_message = state.messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

    return "end"


def error_node(state: AgentState) -> dict:
    """Handle unrecoverable errors."""
    logger.error("workflow_error", error=state.error)
    return {
        "current_step": "error",
        "messages": [
            HumanMessage(
                content=f"The workflow encountered an error: {state.error}. "
                "Please check the logs for details."
            )
        ],
    }


def build_graph(
    config: AgentConfig | None = None,
    tools: list | None = None,
    system_prompt: str | None = None,
) -> StateGraph:
    """Build the LangGraph workflow for the DevOps agent.

    Args:
        config: Agent configuration (unused currently, kept for API compat).
        tools: Tool list to bind to the LLM. Defaults to REVIEW_TOOLS.
        system_prompt: Custom system prompt. Defaults to the PR review prompt.

    Returns:
        A compiled LangGraph StateGraph.
    """
    active_tools = tools or REVIEW_TOOLS

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("reasoning", _make_reasoning_node(active_tools, system_prompt, config))
    graph.add_node("tools", ToolNode(active_tools))
    graph.add_node("error", error_node)

    # Entry point
    graph.set_entry_point("reasoning")

    # Conditional routing from reasoning
    graph.add_conditional_edges(
        "reasoning",
        should_continue,
        {
            "tools": "tools",
            "end": END,
            "error": "error",
        },
    )

    # After tool execution, always go back to reasoning
    graph.add_edge("tools", "reasoning")

    # Error is terminal
    graph.add_edge("error", END)

    return graph.compile(recursion_limit=10)
