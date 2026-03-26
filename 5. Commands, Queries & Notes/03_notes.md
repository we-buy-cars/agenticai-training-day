# Notes — Key Concepts and Reference

Quick reference for the concepts covered in the training session.

---

## Skills = Reusable Expert Knowledge

Skills are instruction files that teach Claude Code how to do specific tasks consistently, following your team's standards every time.

| Skill | What It Does |
|-------|-------------|
| **Ticket Writing Skill** | Enforces your team's ticket template, adds acceptance criteria, references related code |
| **Code Review Skill** | Checks for your coding standards, security patterns, and naming conventions |
| **Test Generation Skill** | Creates tests matching your framework, coverage requirements, and edge case patterns |
| **Documentation Skill** | Generates docs in your format — API specs, architecture decisions, runbooks |

---

## Plugins — Install Superpowers in Seconds

Plugins are installable bundles of skills, commands, and tool integrations. One click to install, instantly available across your team.

| Plugin | What It Does |
|--------|-------------|
| **Skill Creator** | Build custom skills by describing what you want. Claude writes the SKILL.md, tests it, and optimises it — you don't write a single line of config |
| **Code Review** | Dispatches parallel agents to review PRs, find bugs, filter false positives, and post ranked in-line comments directly on GitHub |
| **Feature Dev** | 7-phase workflow: requirements, codebase exploration, architecture, implementation, testing, review, and documentation — all automated |

340+ plugins and 1,300+ skills available — or build your own in minutes.

---

## Worktrees — Parallel Agents, Zero Conflicts

Each agent gets its own isolated copy of the repository. They work in parallel without stepping on each other's changes.

- No context bleed between agents
- Auto-cleanup when done
- Start with `--worktree` or `-w` flag

**Example:** Three agents running simultaneously:
- Agent 1: Fix auth bug
- Agent 2: Add feature
- Agent 3: Write tests

---

## Code Review — AI That Actually Finds Bugs

1. **PR Opens** — Automatically triggered or via `@claude review` comment
2. **Parallel Agents** — Multiple agents scan for different bug categories simultaneously
3. **Verify & Filter** — False positives are eliminated, only real issues remain
4. **Ranked Report** — Bugs posted as in-line comments, ranked by severity

What makes this different from other review tools:
- It reads the full codebase context, not just the diff
- It understands intent — catches logical bugs, not just style issues
- Posts directly to GitHub as actionable in-line comments

---

## The SDLC: Before Claude vs After Claude

| Phase | Before Claude | After Claude |
|-------|--------------|-------------|
| Requirements & Refinement | 2-3 sprint meetings (~2 weeks) | Claude + BA in one session (~2 hours) |
| Ticket Writing | BA writes, dev rewrites, QA adds criteria (~3 days) | Claude drafts complete tickets from epic (~30 min) |
| Development | One dev, one feature, sequential (~1 week) | 3 worktree agents in parallel (~1 day) |
| Code Review | Wait for reviewer, back-and-forth (~2 days) | Code Review plugin + human approval (~2 hours) |
| Testing | Manual test plan, write tests, run them (~3 days) | Claude generates tests from AC (~3 hours) |
| Documentation | "We'll do it later" (never) | Auto-generated with the code (~0 effort) |
| **Total** | **~4 weeks** | **~3 days** |

---

## A Day with Claude Code

| Time | Activity | Role |
|------|----------|------|
| 09:00 | Write tickets from vague requirements | BA |
| 09:30 | Spin up 3 worktree agents for parallel dev | Dev |
| 10:00 | PR auto-reviewed by Code Review plugin | Auto |
| 10:15 | Generate test plans from acceptance criteria | QA |
| 10:30 | Custom skill writes regression tests | QA |
| 11:00 | Feature shipped with docs, tests, and review | Team |

> From ticket to shipped feature in a single morning — across all three roles.

---

## FAQ

### Developers
- **Does it send my code to the cloud?** — Yes, code context is sent to Anthropic's API for processing, but Anthropic does not train on your data. Enterprise plans offer additional data governance.
- **Can it work with our specific tech stack?** — Claude Code is language and framework agnostic — it reads your actual files, so it adapts to whatever you're using.
- **Will it just generate buggy code I have to fix?** — It iterates. You can push back, ask it to debug its own output, and it will run tests to verify before finishing.
- **How is this different from GitHub Copilot?** — Copilot autocompletes lines. Claude Code reads your entire codebase, understands architecture, writes across files, and executes commands.

### Business Analysts
- **I'm not technical — can I still use this?** — Absolutely. You describe what you need in plain English. Claude Code handles the technical translation. It's like having a developer sitting next to you.
- **Can it read our existing documentation?** — Yes. Point it at your codebase, wiki exports, or spec files and it will use that context to write better tickets and requirements.
- **How do I know the output is accurate?** — Claude Code references actual code and data models. It shows its reasoning, so you can verify. Always review — it's a partner, not a replacement.
- **Will this replace BAs?** — No. It amplifies your expertise. You still make the decisions — Claude Code just eliminates the tedious formatting, research, and translation work.

### QA Engineers
- **Can it write automated tests, not just manual ones?** — Yes. It writes unit tests, integration tests, and E2E tests in your framework — NUnit, xUnit, Playwright, Selenium, whatever you use.
- **How does it know what edge cases to test?** — It reads the actual code paths, identifies boundary conditions, null checks, race conditions, and error handling — things humans often miss on first pass.
- **Can it help with regression testing?** — Absolutely. Describe what changed, and it generates targeted regression tests that cover the affected code paths specifically.
- **Does it understand our test data requirements?** — You can teach it via skills. Create a skill with your test data patterns, naming conventions, and environment setup — it follows them every time.

### The Tough Questions
- **What about hallucinations / wrong answers?** — It happens. That's why you verify. But Claude Code can run its own code and check its work — it catches most errors through iteration. Treat it like a junior dev: review everything.
- **What's the cost?** — Anthropic offers team and enterprise plans. The ROI is measured in hours saved per developer per week — typically 5-10 hours reclaimed.
- **Is our code safe / what about IP?** — Anthropic doesn't train on your data. Enterprise plans include SOC 2 compliance and data retention controls. Check your organisation's AI policy.
- **Why not just use ChatGPT / free tools?** — Claude Code runs in your terminal, reads files, and iterates autonomously. ChatGPT is a chat window you copy-paste into. Different paradigm.
