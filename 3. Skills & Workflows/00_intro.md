# Claude Code Skills — An Introduction

## What are Skills?

A **skill** is a reusable set of instructions that teaches Claude how to do a specific task — like a recipe card you hand to an assistant.

Instead of explaining the same task every time, you write the instructions once and give it a name. Then you just say **"do the thing"** and Claude follows the recipe.

## Analogy

Think of it like speed dial on a phone:

- **Without skills:** You type out the full number every time you want to call someone
- **With skills:** You press one button and the call is made

## What does a skill look like?

A skill is just a **text file** with instructions. At its simplest:

```
Name: /deploy
Instructions: "Run the build, run the tests, push to staging"
```

When you type `/deploy`, Claude reads those instructions and executes them step by step.

## Why use them?

1. **Save time** — no re-explaining repetitive workflows
2. **Consistency** — the task is done the same way every time
3. **Shareable** — others on your team can use your skills too

## Real-world examples

| Skill | What it does |
|-------|-------------|
| `/commit` | Creates a git commit with a well-formatted message |
| `/create-branch` | Makes a new branch following your team's naming convention |
| `/merge-down` | Merges your work into shared branches the right way |

## The key idea

> You're not writing code. You're writing **instructions in plain English** that Claude follows every time you invoke the skill.
