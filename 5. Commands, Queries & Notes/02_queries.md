# Queries — Prompts and Questions by Role

Claude Code isn't just for developers. Here are example queries for every role, showing how to get the most out of it.

---

## Developer Queries

### Writing & Debugging Code

Claude Code reads your entire codebase, understands architecture and patterns, writes and edits code directly, debugs by reading errors and context, and iterates until the solution works.

**The development workflow:**

1. Describe the task
2. Claude reads your code
3. Writes a solution
4. Tests and debugs
5. Working code

**Example prompts:**

```
The monthly report shows stale data after refresh. Find the caching bug, fix it, and write a regression test.
```

```
Add pagination to the /api/vehicles endpoint. Follow the existing pattern in /api/auctions.
```

```
Refactor the pricing module to use the strategy pattern. Keep all existing tests passing.
```

### Writing Better Tickets (for devs writing their own)

Claude Code reads your codebase, identifies root cause (not just symptoms), writes structured tickets with clear title, context, acceptance criteria, and edge cases, and includes how to verify the fix — QA-ready from day one.

```
Read the VehicleService and write a bug ticket for the stale cache issue. Include acceptance criteria and edge cases.
```

---

## Business Analyst Queries

### Writing Tickets & User Stories

```
Draft a user story: Users on the WBC website must be able to save a vehicle to a favourites list so they can come back to it later.
```

```
Create a User Story in Azure DevOps: Title: Save vehicle to favourites list. Description: Users on the WBC website must be able to save a vehicle to a favourites list to revisit later. Product: WBC Website
```

### Extracting Stories from Documents

```
Please read this document and extract all the requirements as separate User Stories using my standard format.
```

### General BA Tasks

```
Summarise this document in 5 bullet points.
```

```
Rewrite this in simpler language for a non-technical stakeholder: "The API endpoint must validate the JWT token on every request before processing the payload."
```

```
Create a Word document: a one-page meeting agenda template for BA stakeholder sessions. Include sections for attendees, discussion points, decisions and actions.
```

---

## QA Engineer Queries

### Test Generation

```
Generate a test plan for the favourites feature based on this acceptance criteria.
```

```
Write Playwright E2E tests for the login flow. Cover happy path, invalid credentials, and session expiry.
```

```
What edge cases should we test for the vehicle search filter? Read the search service code first.
```

### Regression Testing

```
The pricing calculation changed in the last commit. Generate regression tests that cover the affected code paths.
```

---

## Prompting Tips — For Everyone

The single most important rule: **the more context you give Claude, the better the output.**

| Vague (avoid) | Specific (do this) |
|---|---|
| Make me a ticket | Create a User Story for the Pricing product. Users must be able to filter by make and model on the WBC app. |
| Fix this | Rewrite this description in plain English for a non-technical audience. |
| Summarise | Summarise this in 3 bullet points focused on what the BA team needs to action. |
