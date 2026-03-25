# Worktrees (Parallel Agents)

Run multiple Claude Code agents simultaneously, each in an isolated copy of your repo:

```bash
# Start Claude Code with a worktree (isolated copy)
claude --worktree

# Or use the short flag
claude -w
```

Each agent gets its own branch, its own working copy, no conflicts. When it's done, review and merge. Like having 3 developers working in parallel without merge hell.
