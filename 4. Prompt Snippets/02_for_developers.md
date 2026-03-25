# Prompt Snippets — For Developers

Copy-paste any of these prompts directly into Claude Code. Replace anything in `[brackets]` with your own details.

---

## Debug an Error

```
I'm getting this error: [paste error message or stack trace]

Read the relevant code files, trace the execution path, explain what's going wrong,
write a fix, and generate a test to prevent regression.
```

---

## Write a New Feature

```
I need to implement: "[describe the feature]"

Read the existing codebase to understand our architecture and patterns, then:
1. Propose an approach (which files to create/modify)
2. Write the implementation following our existing patterns
3. Write unit tests for all new public methods
4. Update any relevant documentation
```

---

## Refactor Existing Code

```
Read [file or folder path] and refactor it to:
- Follow SOLID principles
- Extract methods longer than 30 lines
- Add proper error handling
- Improve naming for clarity
- Add missing documentation comments

Show me the before/after for each change and explain why it's better.
Keep all existing tests passing.
```

---

## Code Review a File

```
Review [file path] against best practices. Check for:
- SOLID violations
- Missing null checks or error handling
- Async/await correctness
- Potential performance issues (N+1 queries, memory leaks)
- Security concerns (SQL injection, XSS, hardcoded secrets)
- Missing tests
- Naming and readability issues
Suggest specific fixes with code examples.
```

---

## Generate Tests for Existing Code

```
Read [file or folder path] and generate comprehensive tests.
Follow our existing test patterns and framework.
Include:
- Happy path tests
- Edge cases (boundary values, empty collections, null inputs)
- Error scenarios (invalid input, exceptions, timeouts)
- Use parameterised tests where multiple inputs test the same behaviour
```

---

## Fix a Failing Test

```
This test is failing: [paste test name or file]

The error is: [paste error output]

Read the test and the source code it's testing.
Explain why it's failing and fix either the test or the source code
(whichever is actually wrong). Don't just make the test pass —
make sure the behaviour is correct.
```
