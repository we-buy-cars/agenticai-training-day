# Claude AI Tooling Session

## Slide 1: Model Differences

Claude has 3 tiers — pick the right one for the job:

| Model | Speed | Intelligence | Cost | Best For |
|-------|-------|-------------|------|----------|
| **Haiku** | Fastest | Good | Cheapest | Quick lookups, classification, simple Q&A, bulk processing |
| **Sonnet** | Balanced | Very Good | Mid-range | Day-to-day coding, analysis, content, most tasks |
| **Opus** | Slowest | Highest | Most expensive | Complex reasoning, architecture decisions, nuanced analysis |

**Key takeaway:** Don't use Opus to format a JSON blob. Don't use Haiku to architect a system. Match the model to the task complexity.

---

## Slide 2: How to Prompt Effectively

**Bad prompt:**
> Fix my code

**Good prompt:**
> I have a C# ASP.NET Core 8 API endpoint that returns a 500 error when the request body contains a null `LeadCode`. The endpoint is `POST /api/leads`. Here's the relevant code: [code]. The error from the logs is: [error]. Fix the null handling and return a proper 400 BadRequest response.

**The formula:**
1. **Context** — What tech, what project, what environment
2. **Specifics** — Exact error, exact file, exact behaviour
3. **Desired outcome** — What "done" looks like
4. **Constraints** — Language, framework version, patterns to follow

**Other tips:**
- Give examples of input/output you expect
- Say "don't explain, just give me the code" if you want concise output
- Use "step by step" for complex reasoning tasks
- Paste error messages verbatim — don't paraphrase
- Tell it your role: "I'm a C# backend dev" changes the response depth

---

## Slide 3: Understanding Tokens

Tokens are how AI reads and bills you. They're word fragments, not words.

- "Hello world" = 2 tokens
- "ChatGPT" = 3 tokens (Chat + G + PT)
- 1 token ≈ 0.75 English words
- 1000 tokens ≈ 750 words ≈ ~1.5 pages of text

**Why it matters:**
- **Input tokens** = what you send (prompt + context + files)
- **Output tokens** = what the model generates back
- You pay for BOTH
- Claude's context window is up to 200K tokens — that's roughly a 300-page book

**Practical tips:**
- Don't paste an entire codebase when you only need help with one method
- Summarise background context instead of dumping raw logs
- Longer prompts ≠ better prompts — be precise, not verbose
- Use system prompts to set persistent context so you don't repeat yourself

---

## Slide 4: Right Model for the Right Job

| Task | Model | Why |
|------|-------|-----|
| Rename 500 variables in a file | Haiku | Mechanical, pattern-based, no deep thinking needed |
| Write unit tests for a service | Sonnet | Needs code understanding but it's a well-known pattern |
| Debug a race condition across 3 microservices | Opus | Complex reasoning across multiple systems |
| Generate a SQL query from a description | Sonnet | Understands schema + intent, standard complexity |
| Classify 10,000 support tickets | Haiku | Bulk classification, fast and cheap |
| Design a new event-driven architecture | Opus | Needs deep trade-off analysis and creativity |
| Summarise a meeting transcript | Sonnet | Comprehension task, doesn't need max intelligence |
| Quick "what does this error mean?" | Haiku | Simple lookup, instant answer |

**Rule of thumb:**
- If a junior dev could do it → **Haiku**
- If a mid-level dev would handle it → **Sonnet**
- If you'd want a senior/architect → **Opus**

---

## Slide 5: Quick Wins — Use These Today

1. **Claude.ai Projects** — Create a project, add your repo docs / schema / standards as context. Every chat in that project knows your codebase.
2. **Custom Instructions** — Set your tech stack, coding style, and preferences once. Every new chat respects them.
3. **Artifacts** — Ask Claude to build you interactive tools (calculators, dashboards, forms) right in the chat.
4. **MCP Tools** — Connect Claude to Dynatrace, Elasticsearch, Azure DevOps, etc. Debug production issues directly from chat.
5. **Claude Code (CLI)** — Run Claude in your terminal. It reads your files, runs commands, writes code directly in your repo.
