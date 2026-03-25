# Plan Mode vs Auto Execute

Claude Code has two modes — you choose the level of control:

| Aspect | Plan Mode | Auto Execute |
|--------|-----------|-------------|
| **How it works** | Claude proposes a plan, you approve before it acts | Claude reads, writes, and runs immediately |
| **Speed** | Slower (you review each step) | Fastest (no approval between actions) |
| **Best for** | Large refactors, architecture changes, unfamiliar code, high-risk work | Bug fixes, test generation, docs, small well-understood changes |
| **Trust level** | "Show me before you touch anything" | "I trust you, just do it" |

**Tip:** Start in Plan Mode while you're learning. Switch to Auto Execute as you build confidence.

To use plan mode, type `shift+tab` to toggle between modes, or type:

```
/plan [describe what you want]
```
