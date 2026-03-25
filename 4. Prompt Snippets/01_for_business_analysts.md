# Prompt Snippets — For Business Analysts

Copy-paste any of these prompts directly into Claude Code. Replace anything in `[brackets]` with your own details.

---

## Write a Ticket from a Vague Request

```
I have a vague requirement: "[paste the vague request here]"

Read the relevant code in our codebase, then write a complete work item with:
- A clear, specific title
- User story format: As a [role], I want [goal], so that [benefit]
- Acceptance criteria (specific and testable)
- Edge cases (at least 3)
- Technical notes referencing actual code files
- Test scenarios mapped to each acceptance criterion
```

---

## Break an Epic into Sprint-Ready Tickets

```
Here's an epic: "[paste epic description]"

Read the relevant areas of our codebase, then break this into sprint-ready work items.
Each ticket should have: title, user story, acceptance criteria, edge cases, technical notes,
estimated complexity (S/M/L), and dependencies on other tickets.
Order them by implementation sequence.
```

---

## Write a Feature Spec / PRD

```
I need a feature spec for: "[describe the feature]"

Read the relevant code to understand our current architecture, then write a PRD with:
- Problem statement (what's broken or missing)
- Proposed solution (how we'll fix or build it)
- User stories with acceptance criteria
- Technical approach (affected files, APIs, data models)
- Out of scope (what this does NOT include)
- Success metrics (how we know it worked)
```

---

## Validate Requirements Against Code

```
Here are the requirements for a feature: "[paste requirements]"

Read the codebase and tell me:
- Which requirements are already partially implemented
- Which ones conflict with the current architecture
- What's missing from the requirements that a developer would need to know
- Suggest improvements to make the requirements more precise
```
