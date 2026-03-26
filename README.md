# Agentic AI Training Day — WeBuyCars

A hands-on training session on how we use Claude Code at WeBuyCars. This repo is your reference guide — everything from installation to building autonomous agents.

## What's This About?

This is an internal WeBuyCars training covering how to use Claude Code effectively across roles — whether you're a developer, business analyst, QA engineer, or just curious. You'll learn efficient prompting, reusable skills, automation patterns, and how to build your own agents.

## Prerequisites

- **Node.js** (v18+) — needed to install Claude Code
- **Anthropic API key** — or access via your WeBuyCars organisation plan
- **Python 3.10+** — only if you're doing the Agent SDK exercises (Section 7)
- A terminal and a code editor (VS Code recommended)

## Getting Started

```bash
git clone https://github.com/we-buy-cars/agenticai-training-day.git
cd agenticai-training-day
npm install -g @anthropic-ai/claude-code
claude
```

## Presentation Slides

- [Claude Code in Action.pdf](Claude%20Code%20in%20Action.pdf) — main presentation deck
- [ClaudeTrainingDay.pdf](ClaudeTrainingDay.pdf) — supplementary training materials

## Repo Structure

| Folder | What's Inside |
|--------|---------------|
| **1. Getting Started** | Install Claude Code, set up your repo, and create your first skill |
| **2. Efficient Prompting** | Model selection, token management, the prompting formula, security rules, and a real-world example (Azure Exam Simulator) |
| **3. Skills, Workflows & Tools** | Reusable skills, multi-step workflows, and automation with `/loop` and `/schedule` |
| **4. Prompt Snippets** | Copy-paste prompts for BAs, developers, QA engineers, and everyone else |
| **5. Commands, Queries & Notes** | Your scratch space — add your own notes during the session |
| **6. Modes & Power Features** | Plan Mode vs Auto Execute, worktrees for parallel work, custom skills and commands |
| **7. Agent SDK** | Build autonomous agents in Python — includes 3 exercises, custom tools, and a buggy app to review |
| **8. Sarel Setup** | Production example: a DevOps PR review agent built with LangGraph |
| **BA Tools** | Claude for Business Analysts — user stories, Azure DevOps integration, document extraction, and prompting tips |
| **QA Tools** | Complete QA automation guides — from zero to Playwright pro with Claude Code |
| **Nice To Haves** | Cheat sheet and security/compliance summary |

## Suggested Path

**Everyone** should start with:

1. [1. Getting Started](1.%20Getting%20Started/) — get Claude Code running
2. [2. Efficient Prompting](2.%20Efficient%20Prompting/) — learn how to prompt well and save tokens
3. [4. Prompt Snippets](4.%20Prompt%20Snippets/) — grab prompts for your role

**Then pick your track:**

- **Business Analysts** → [BA Tools](BA%20tools/) (user stories, DevOps integration, document extraction)
- **Developers** → [3. Skills, Workflows & Tools](3.%20Skills%2C%20Workflows%20%26%20Tools/) → [6. Modes & Power Features](6.%20Modes%20%26%20Power%20Features/)
- **QA Engineers** → [QA Tools](QA%20tools/) (start with the getting started guide)
- **Agent Builders** → [7. Agent SDK](7.%20Agent%20SDK/) → [8. Sarel Setup](8.%20Sarel%20Setup/)

## Key Takeaways

- **Pick the right model** — Haiku for simple tasks, Sonnet for everyday work, Opus for complex reasoning
- **Prompt with structure** — context, specifics, desired outcome, constraints
- **Use CLAUDE.md** — persistent project context saves tokens and improves results
- **Build skills** — reusable instructions that make Claude Code work the way your team needs
- **Stay secure** — never paste credentials, anonymize data, review skills before enabling

## Quick Reference

See [Nice To Haves/01_cheat_sheet.md](Nice%20To%20Haves/01_cheat_sheet.md) for a one-page table of common tasks and prompts.

## Security

Claude Code is SOC 2 Type II certified. Anthropic does not train on your code. See [Nice To Haves/02_security.md](Nice%20To%20Haves/02_security.md) for the full breakdown.
