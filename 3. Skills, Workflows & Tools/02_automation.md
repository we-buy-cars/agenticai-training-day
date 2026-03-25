# Automation — Loop & Schedule

Claude Code has two built-in ways to run skills automatically: **loop** for short-lived repetition and **schedule** for long-lived recurring jobs.

## Loop — "Keep doing this"

Loop runs a skill (or any prompt) repeatedly on an interval, right inside your current session.

**When to use it:** You're actively working and want Claude to keep checking something while you focus on other things.

**How it works:**

```
/loop 5m /investigate
```

This runs `/investigate` every 5 minutes until you stop it. Think of it like setting a kitchen timer that keeps restarting.

**Examples:**

| Command | What it does |
|---------|-------------|
| `/loop 5m /investigate` | Check logs for errors every 5 minutes |
| `/loop 10m check the deploy status` | Monitor a deployment every 10 minutes |
| `/loop 2m are there new PR comments?` | Watch for feedback on your pull request |

**Key points:**
- Runs inside your current Claude Code session
- Stops when you close the session or tell it to stop
- Default interval is 10 minutes if you don't specify one
- Great for monitoring something while you work

## Schedule — "Do this every day/week"

Schedule creates a recurring job that runs on a cron schedule — even when you're not at your computer.

**When to use it:** You want something to happen automatically on a regular basis, like a daily or weekly task.

**How it works:**

```
/schedule "every weekday at 9am, check for unresolved PR comments"
```

This creates a background agent that wakes up on schedule, does the work, and goes back to sleep. Think of it like a calendar reminder that actually does the task for you.

**Examples:**

| Schedule | What it does |
|----------|-------------|
| Every weekday at 9am | Check for PR comments and flag them |
| Every Friday at 4pm | Summarise the week's closed PRs |
| Every Monday at 8am | List open PRs that need review |

**Key points:**
- Runs in the background, even when Claude Code is closed
- Uses cron syntax under the hood, but you can describe the schedule in plain English
- Each scheduled job is a standalone agent — it starts fresh each time

## Loop vs Schedule — When to use which

| | Loop | Schedule |
|---|------|----------|
| **Duration** | While your session is open | Indefinitely |
| **Trigger** | Timer interval (e.g. every 5m) | Cron schedule (e.g. daily at 9am) |
| **Use case** | Active monitoring | Recurring automation |
| **Analogy** | Refreshing a webpage | A daily alarm |

## The key idea

> **Loop** is for watching something right now. **Schedule** is for automating something forever.
