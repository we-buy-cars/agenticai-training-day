# DevOps Agent - Graph Flows

## PR Review Graph

The current implementation uses the **ReAct pattern** (Reason → Act → Observe → repeat).
Claude reasons, picks a tool, observes the result, reasons again until it produces a final answer.

```mermaid
flowchart TD
    START([START]) --> reasoning

    reasoning["🧠 reasoning_node\nClaude LLM call\nDecides next action"]

    reasoning --> should_continue{should_continue?}

    should_continue -->|has tool_calls| tools
    should_continue -->|no tool_calls| END([END])
    should_continue -->|max retries hit| error

    tools["⚙️ ToolNode\nfetch_pr_details\nanalyze_code\nformat_review_comments\ncheck_appconfig_key"]

    tools --> reasoning

    error["❌ error_node\nLog + append\nerror message"] --> END
```
