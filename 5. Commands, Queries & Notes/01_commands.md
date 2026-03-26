# Commands — One-Click Workflows

Slash commands are shortcuts you type in Claude Code to trigger a predefined workflow instantly. Think of them as macros that kick off a sequence of steps with one action.

## Built-in Slash Commands

| Command | What It Does |
|---------|-------------|
| `/review-pr` | Reviews a pull request against your team's standards |
| `/write-spec` | Generates a full PRD from a feature idea |
| `/debug` | Investigates an error with full codebase context |
| `/test` | Generates comprehensive tests for a module |
| `/document` | Creates documentation in your team's format |

You can create custom commands tailored to your team's specific workflows.

## How Commands Work

1. You type the command (e.g. `/review-pr`)
2. Claude Code loads the associated skill or instruction set
3. It runs through the predefined steps automatically
4. You get structured output without writing a detailed prompt every time

## Commands vs Skills

| | Skill | Command |
|---|-------|---------|
| **What it is** | A markdown instruction file that teaches Claude Code how to do something — persistent expert knowledge | A shortcut that triggers a specific workflow instantly — a button that runs predefined steps |
| **Think of it as** | A playbook or standard operating procedure that Claude follows automatically | A shortcut key or macro that kicks off a workflow with one action |

> A skill is the knowledge. A command is the trigger. Commands often use skills under the hood.

## Example: Custom Ticket Writing Command

You could create a `/write-ticket` command that:
1. Reads your team's ticket template (from a skill)
2. Asks for the requirement
3. Generates a structured ticket with title, description, acceptance criteria, and edge cases
4. Formats it ready for Azure DevOps

## Try It

```
/review-pr
```

```
/test src/services/pricing.ts
```

```
/debug "The monthly report shows stale data after refresh"
```
