# Claude Code Power User Guide

This guide is for QA engineers who already use Claude Code and want to get significantly more out of it. We cover the tools, configuration, and workflows that separate casual use from daily productivity. Everything here is practical and business-focused — no theory, just patterns that make QA work faster.

**Assumes:** You've installed Claude Code, run a few prompts, and written at least one test with it.

---

## 1. Where Claude Code Runs

Claude Code works in different environments. Each has trade-offs for QA work.

### Terminal (Standalone)

```bash
claude
```

Launch from any directory. Full access to all features, no IDE dependency. Best for: headless environments, CI pipelines, SSH sessions, or when you want zero distractions.

### VS Code Extension

Install the **Claude Code** extension from the VS Code marketplace. Opens as a sidebar panel. Best for: seeing code changes in real-time as Claude edits files, inline diff review, and quick file navigation alongside the conversation.

### JetBrains Plugin (PyCharm, IntelliJ, etc.)

Install via **Settings > Plugins > Marketplace > Claude Code**. Runs in a tool window panel. Best for: PyCharm users who want Claude Code without leaving their IDE. Same features as VS Code integration.

**Bottom line:** All three environments share the same Claude Code engine and capabilities. The terminal gives you the most control. IDE integrations give you visual context. Use whichever fits your workflow — you can switch freely.

---

## 2. Core Tools

Claude Code doesn't just generate text — it has dedicated tools for interacting with your codebase. Understanding what's available helps you write better prompts.

### File Operations

| Tool | What it does | QA example |
|------|-------------|------------|
| **Read** | Reads file contents | "Read the conftest.py and explain the fixtures" |
| **Edit** | Makes targeted edits (find & replace) | "Change the timeout from 5000 to 10000 in the login test" |
| **Write** | Creates new files or full rewrites | "Create a new test file for the checkout flow" |
| **Glob** | Finds files by pattern | "Find all test files in the project" |
| **Grep** | Searches file contents with regex | "Find everywhere we use `page.wait_for_timeout`" |

### Bash

Runs shell commands directly. Claude Code uses this for:
- Running your tests (`pytest test_login.py -v -s`)
- Git operations (`git status`, `git diff`)
- Installing packages (`pip install faker`)
- Any terminal command you'd normally type yourself

**Key point:** When you say "run my test", Claude Code uses Bash. When you say "read my test file", it uses Read. When you say "fix the timeout in my test", it uses Edit. Knowing this helps you understand what Claude Code is doing and why it asks for permission.

---

## 3. Slash Commands & Skills

Slash commands are shortcuts that trigger specific behaviors. Type them directly in the Claude Code prompt.

### Built-in Commands

| Command | What it does |
|---------|-------------|
| `/help` | Show available commands and usage tips |
| `/clear` | Clear conversation history and start fresh |
| `/compact` | Compress conversation to save context window space |
| `/status` | Show current model, context usage, and settings |
| `/cost` | Show token usage and cost for current session |

### Skills (Custom Slash Commands)

Skills are project-specific commands defined in your configuration. They expand into full prompts when invoked.

```
/commit          — stage changes and create a commit with a good message
/review-pr 123   — review a pull request by number
```

Skills are powerful because they encode complex workflows into a single command. Instead of writing a 10-line prompt every time you want to commit, `/commit` does it consistently.

**How skills work:** When you type a slash command, Claude Code looks it up in the available skills, expands it into a full prompt with instructions, and executes it. The skill definition tells Claude Code exactly what tools to use, what format to follow, and what output to produce.

**Creating custom skills:** Skills are defined in your project's `.claude/` directory or in your global Claude Code config. Each skill is a markdown file with a prompt template. See the [official docs](https://docs.anthropic.com/en/docs/claude-code/slash-commands) for the full spec.

---

## 4. Agents

Agents are specialized sub-processes that Claude Code launches to handle complex tasks autonomously. Think of them as assistants that Claude Code delegates work to.

### How Agents Work

When a task requires deep research, multiple file searches, or parallel exploration, Claude Code spawns an agent. The agent gets its own context, runs independently, and reports back with results.

```
"Search the entire codebase for every place we handle login timeouts
and summarize the different approaches"
```

Claude Code might spawn an **Explore agent** for this — it searches files, reads relevant code, and returns a summary without cluttering your main conversation.

### Agent Types

| Type | Purpose | When Claude Code uses it |
|------|---------|------------------------|
| **Explore** | Fast codebase search and analysis | Finding files, searching code, answering "how does X work?" |
| **General-purpose** | Complex multi-step research | Tasks requiring many searches, web lookups, or file reads |
| **Plan** | Architecture and implementation planning | Designing test strategies, planning refactors |

### Background Agents

Agents can run in the background while you continue working. Claude Code notifies you when they finish.

```
"In the background, search all test files for hardcoded waits
(wait_for_timeout) and list them with file paths and line numbers"
```

You keep working on your current task. The agent reports back when done.

### Parallel Agents

Multiple agents can run simultaneously for independent tasks:

```
"Search for all uses of nexus_login() AND separately find all
screenshot fixtures in the project"
```

Claude Code launches two agents in parallel — one for each search — and combines the results.

**QA use case:** Before writing tests for a new page, ask Claude Code to explore the page structure AND search for existing test patterns for similar pages. Both run in parallel, and you get context from two angles at once.

---

## 5. Permissions & Trust Levels

Claude Code asks for permission before taking actions. Understanding the permission system lets you speed up repetitive workflows without sacrificing safety.

### The Three Permission Levels

| Level | Behavior | Example tools |
|-------|----------|--------------|
| **Auto-allow** | Runs without asking | Read, Glob, Grep (read-only tools) |
| **Prompt** | Asks you each time | Edit, Write, Bash (modifying tools) |
| **Deny** | Blocked entirely | Tools you've explicitly forbidden |

### Allowlisting Commands

Tired of approving `pytest` every time? Allowlist it:

**Project-level** (`.claude/settings.json` — shared with team):
```json
{
  "permissions": {
    "allow": [
      "Bash(pytest *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)"
    ]
  }
}
```

**User-level** (`~/.claude/settings.json` — your machine only):
```json
{
  "permissions": {
    "allow": [
      "Bash(pip install *)",
      "Bash(playwright install *)",
      "Edit(*)"
    ]
  }
}
```

### Project vs Global Settings

| File | Scope | Use for |
|------|-------|---------|
| `.claude/settings.json` | This project, all users | Team conventions: allowlisted test commands, shared permissions |
| `~/.claude/settings.json` | All projects, this user | Personal preferences: edit permissions, package installs |
| `.claude/settings.local.json` | This project, this user only | Project-specific overrides you don't want to share |

### Practical Allowlist for QA

A sensible starting point for QA automation projects:

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest *)",
      "Bash(.venv/Scripts/python.exe -m pytest *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git add *)",
      "Bash(pip install *)",
      "Bash(pip list)",
      "Bash(playwright install *)"
    ]
  }
}
```

This auto-approves test runs, git read operations, and package management — the commands you run dozens of times per session. Edits, writes, and destructive git operations still prompt for approval.

---

## 6. Hooks

Hooks are shell commands that run automatically before or after Claude Code uses a tool. They let you enforce rules, run checks, and automate side effects.

### How Hooks Work

Hooks are defined in your settings files and trigger on tool events:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "echo 'File written: check for sensitive data'"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "echo 'About to run a command'"
      }
    ]
  }
}
```

### Hook Events

| Event | When it fires | Use case |
|-------|--------------|----------|
| **PreToolUse** | Before a tool runs | Validate inputs, block dangerous commands |
| **PostToolUse** | After a tool completes | Run linters, format code, notify systems |
| **UserPromptSubmit** | When you send a message | Pre-process prompts, add context |

### QA-Relevant Hook Examples

**Auto-format Python files after edits:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "command": "black --quiet $CLAUDE_FILE_PATH 2>/dev/null || true"
      }
    ]
  }
}
```

**Block accidental production database commands:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "echo $CLAUDE_TOOL_INPUT | grep -qi 'production' && echo 'BLOCKED: production command detected' && exit 1 || exit 0"
      }
    ]
  }
}
```

**Key point:** Hooks give you guardrails. In QA work, they're useful for preventing accidental data modifications, auto-formatting test code, and enforcing team conventions without relying on memory.

---

## 7. MCP Servers (Model Context Protocol)

MCP servers extend Claude Code's capabilities by connecting it to external tools and services. Think of them as plugins.

### What MCP Servers Do

An MCP server exposes tools that Claude Code can call, just like its built-in tools. The difference: MCP tools connect to external systems.

**Examples of what MCP servers can provide:**
- Database query tools (run SQL against staging databases)
- Jira/Azure DevOps integration (read tickets, update status)
- Slack integration (post test results to a channel)
- Browser automation tools (beyond Playwright)
- Custom API clients (hit your staging endpoints directly)

### Configuration

MCP servers are configured in your settings:

```json
{
  "mcpServers": {
    "my-db-server": {
      "command": "node",
      "args": ["path/to/mcp-server.js"],
      "env": {
        "DB_CONNECTION": "your-connection-string"
      }
    }
  }
}
```

Once configured, the MCP server's tools appear alongside Claude Code's built-in tools. You use them the same way — describe what you want and Claude Code picks the right tool.

### QA Use Case

An MCP server connected to your staging database lets you say:

```
"Query the staging database for the last 5 leads created today
and check if their finance applications have been submitted"
```

Claude Code calls the MCP server's query tool instead of you switching to a SQL client, writing the query, and reading the results manually.

**Getting started with MCP:** See the [official MCP documentation](https://docs.anthropic.com/en/docs/claude-code/mcp-servers) for available servers and how to build your own.

---

## 8. Memory System

Claude Code's memory system lets it remember information across conversations. Without memory, every new conversation starts from zero. With memory, Claude Code builds up knowledge about you, your project, and your preferences over time.

### How It Works

Memory lives in your project's `.claude/projects/<project-hash>/memory/` directory. It consists of:
- **MEMORY.md** — an index file that's loaded into every conversation automatically
- **Individual memory files** — markdown files with frontmatter, linked from MEMORY.md

### The Four Memory Types

#### User Memories

Information about you — your role, expertise, preferences, and working style.

```markdown
---
name: user_role
description: George's role and expertise areas
type: user
---

Senior QA engineer. Deep Playwright + Python expertise. Prefers terse output,
no trailing summaries. Wants raw technical details, not simplified explanations.
```

**When Claude Code saves these:** When it learns about your role, preferences, or knowledge level.
**How it uses them:** Tailors responses to your expertise. Won't over-explain Playwright to a senior engineer. Won't skip basics for a junior.

#### Feedback Memories

Corrections and guidance you've given Claude Code. These are the most important type — they prevent repeated mistakes.

```markdown
---
name: feedback_no_mocks
description: Integration tests must use real database, not mocks
type: feedback
---

Integration tests must hit the real staging database, not mocks.

**Why:** Prior incident where mocked tests passed but the production migration failed.
Mocks masked a schema divergence that caused a 4-hour outage.

**How to apply:** When writing database-related tests, always use the real
db_helper.py connection. Never suggest mocking DB calls in test files.
```

**When Claude Code saves these:** When you correct its approach — "don't do X, do Y instead."
**How it uses them:** Applies the correction in every future conversation. You correct once, not repeatedly.

#### Project Memories

Ongoing work context — what's being built, why, deadlines, decisions.

```markdown
---
name: project_release_freeze
description: Merge freeze starting March 5 for mobile release
type: project
---

Merge freeze begins 2026-03-05 for mobile release branch cut.

**Why:** Mobile team needs a stable branch. Non-critical merges blocked until 2026-03-08.

**How to apply:** Flag any non-critical PR work scheduled after March 5.
Prioritize critical bug fixes that need to land before the freeze.
```

**When Claude Code saves these:** When it learns about deadlines, decisions, or work context that affects future conversations.
**How it uses them:** Avoids suggesting work that conflicts with project constraints.

#### Reference Memories

Pointers to where information lives in external systems.

```markdown
---
name: ref_bug_tracker
description: Pipeline bugs tracked in Linear project INGEST
type: reference
---

Pipeline bugs are tracked in the Linear project "INGEST".
Test failures related to data ingestion should reference this project.
QA board for test tracking is in Azure DevOps under the QA project.
```

**When Claude Code saves these:** When you mention external tools, dashboards, or systems.
**How it uses them:** Knows where to point you for information it can't access directly.

### Managing Memory

**Ask Claude Code to remember:**
```
"Remember that our staging DB requires MFA — use ActiveDirectoryInteractive auth"
```

**Ask Claude Code to forget:**
```
"Forget the memory about the merge freeze — that's over now"
```

**Check what it remembers:**
```
"What do you remember about our database setup?"
```

Claude Code reads the relevant memory files and responds with what it knows.

---

## 9. CLAUDE.md — Advanced Patterns

The [Getting Started guide](getting_started_guide.md) covers basic CLAUDE.md setup. Here's how to make it powerful.

### Rules That Enforce Consistency

```markdown
## Rules
1. All test files must use fixtures from conftest.py — never create browser instances directly
2. Screenshots go in the ticket's screenshots/ directory, nowhere else
3. Use get_by_role() for buttons and links, get_by_placeholder() for inputs
4. Never hardcode test data — use Faker or data_generators.py
5. Every test function name starts with test_ and describes the behavior being tested
```

Rules in CLAUDE.md are read at the start of every conversation. They're stronger than per-conversation instructions because they persist.

### Documenting Shared Modules

```markdown
## Shared Modules
- **helpers/login.py** — `login(page, user, password)` handles OAuth flow + MFA
- **helpers/data.py** — `generate_user()` returns dict with name, email, phone, ID number
- **helpers/screenshots.py** — `capture(page, name)` saves to ticket screenshots/ dir
```

When you say "use the login helper", Claude Code knows exactly which function to call and what arguments it takes.

### Environment and Commands

```markdown
## Commands
# Run all tests
pytest tests/ -v -s

# Run a specific test file
pytest tests/test_login.py -v -s

# Run tests matching a keyword
pytest -k "checkout" -v -s
```

Claude Code uses these exact commands when you say "run my tests" — no guessing.

### Context Management

CLAUDE.md is loaded into every conversation. Keep it focused:
- Put stable information here (conventions, commands, module docs)
- Don't put temporary task details (use memory or conversation context instead)
- Link to detailed docs rather than duplicating content
- Review and trim periodically — a bloated CLAUDE.md wastes context window

---

## 10. Keyboard Shortcuts & Terminal Tips

Quick reference for navigating Claude Code efficiently.

### Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message (single line) |
| `Shift+Enter` | New line (multi-line input) |
| `Escape` | Cancel current generation / dismiss |
| `Ctrl+C` | Interrupt running tool or exit |
| `Up Arrow` | Recall previous message |
| `Tab` | Accept autocomplete suggestion |

### Useful Commands

| Command | What it does |
|---------|-------------|
| `/clear` | Wipe conversation, start fresh |
| `/compact` | Compress history to save context space |
| `/status` | Show model, context usage, config |
| `/cost` | Token usage and cost this session |
| `/help` | Available commands and usage |
| `/model` | Switch between models (Opus, Sonnet, Haiku) |

### Context Window Tips

Claude Code has a finite context window. Long conversations hit limits. Manage it:

- **Use `/compact` proactively** — don't wait until you hit the limit. Compact after completing a task before starting the next one.
- **Use `/clear` between unrelated tasks** — starting fresh is faster than carrying irrelevant context.
- **Let agents handle deep searches** — agent results get summarized before entering your context, keeping it clean.
- **Keep CLAUDE.md lean** — it's loaded every conversation. Every unnecessary line costs context.

---

## 11. Where to Go Next

- **[Getting Started guide](getting_started_guide.md)** — if you skipped the basics, start here
- **[Tips & Tricks](claudecode_training_tips_and_tricks.md)** — advanced prompting patterns, debugging workflows, shared framework usage
- **[Official Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/overview)** — full feature reference
- **[MCP Server docs](https://docs.anthropic.com/en/docs/claude-code/mcp-servers)** — extending Claude Code with external tools
- **[Playwright Python docs](https://playwright.dev/python/)** — the automation library underneath it all

> **The best way to learn Claude Code is to use it on real work.** Pick one repetitive task from your day — running a test suite, looking up a lead, checking database state — and let Claude Code handle it. Notice what slows you down (permission prompts, repeated instructions, missing context) and fix it with the tools in this guide: allowlists, memory, CLAUDE.md rules, and skills.