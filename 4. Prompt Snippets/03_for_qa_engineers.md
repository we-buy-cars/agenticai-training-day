# Prompt Snippets — For QA Engineers

Copy-paste any of these prompts directly into Claude Code. Replace anything in `[brackets]` with your own details.

---

## Generate a Test Plan from a Ticket

```
Here's a work item / user story: "[paste ticket]"

Read the relevant code, then create a test plan with:
- Test scenarios mapped to each acceptance criterion
- Edge cases the developer might have missed
- Negative tests (what should NOT happen)
- Data requirements (what test data is needed)
- Environment considerations (what needs to be configured)
Prioritise by risk: high-risk scenarios first.
```

---

## Write Automated Tests from Manual Test Cases

```
Here are our manual test cases: "[paste test cases]"

Read the codebase, find the relevant code, and convert these into
automated tests using our existing test framework and patterns.
Include setup/teardown, test data creation, and assertions
that match the expected outcomes from the manual tests.
```

---

## Generate Regression Tests for a Change

```
This PR/commit changes: "[describe what changed or paste the diff]"

Read the affected code and generate regression tests that:
- Cover all modified code paths
- Test boundary conditions introduced by the change
- Verify existing functionality still works
- Include both positive and negative scenarios
```

---

## Review Test Coverage

```
Read [file or folder path] and our existing tests.
Identify:
- Public methods with no tests
- Code paths not covered (error handlers, edge cases, null checks)
- Tests that exist but don't assert meaningful behaviour
- Suggest specific tests to fill each gap
Prioritise by risk — what would hurt most if it broke?
```
