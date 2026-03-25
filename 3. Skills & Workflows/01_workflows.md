# Skill Workflows — Skills That Call Other Skills

## The idea

A skill doesn't have to do everything itself. It can **call other skills** as steps in a larger workflow — like a manager delegating tasks to specialists.

## Analogy

Think of it like a head chef in a kitchen:

- The **head chef** (workflow skill) doesn't cook every dish personally
- They tell the **pastry chef** to make dessert, the **grill chef** to cook the steak, and the **sous chef** to plate everything
- Each chef knows their job — the head chef just coordinates

## What does this look like?

Say you want a skill that deploys your code end-to-end. Instead of writing all the steps from scratch, you chain existing skills together:

```
Skill: /deploy

Steps:
1. Run /merge-down to merge the feature branch into staging
2. Run /create-prs to open pull requests
3. Notify the team
```

Each step is a skill that already exists and already works. The workflow skill just says **what order to run them in**.

## Why is this powerful?

1. **Reuse** — each skill is written and tested once, then used in many workflows
2. **Composability** — mix and match skills like building blocks
3. **Simplicity** — each skill stays small and focused; complexity lives in the orchestration, not the individual pieces

## A real example

Here's a workflow skill that handles the full PR lifecycle:

```
Skill: /create-prs

Steps:
1. /merge-down → merge feature branch to development and staging
2. Push all branches
3. Create PRs on Azure DevOps for each target branch
```

The `/create-prs` skill doesn't know *how* to merge branches — it just asks `/merge-down` to do it. Each skill is an expert at one thing.

## The pattern

```
┌─────────────────────┐
│   Workflow Skill     │  ← orchestrates the process
│                      │
│  1. /skill-a         │  ← does one thing well
│  2. /skill-b         │  ← does another thing well
│  3. /skill-c         │  ← does yet another thing well
│                      │
└─────────────────────┘
```

## Key takeaway

> Skills are building blocks. Workflow skills are the blueprint that arranges them. Keep each skill focused on one job, then compose them into powerful workflows.
