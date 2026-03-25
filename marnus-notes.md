Claude Skills 
 

 1. Create a Skills Folder 

In your project root, create something like: 

/claude-skills/ 

or if you're using agent frameworks: 

/.claude/skills/ 

Shape 

 2. Create a Skill File 

Most setups use YAML or JSON. 

Example: refactor-code.yaml 

name: refactor-code 
description: Refactor code for readability and performance 
 
input_schema: 
  type: object 
  properties: 
    code: 
      type: string 
      description: The code to refactor 
 
prompt: | 
  You are a senior software engineer. 
 
  Refactor the following code to: 
  - Improve readability 
  - Reduce complexity 
  - Follow best practices 
 
  Code: 
  {{code}} 
 
  Return only the improved code. 

 

3. Register / Load the Skill 

 

…. 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

Claude Code Cheat Sheet 

Copy-paste any of these prompts directly into Claude Code. Replace anything in [brackets] with your own details. 

 

Getting Started (3 Steps) 

# 1. Install 
npm install -g @anthropic-ai/claude-code 
 
# 2. Open your terminal in any repo 
cd your-project/ 
 
# 3. Start Claude Code 
claude 
 

That's it. No config, no SDK, no CI/CD changes required. 

 

Setting Up Your Repo (Optional but Powerful) 

Paste this into Claude Code and it will create a CLAUDE.md file tailored to your project: 

Read our codebase — look at the folder structure, languages, frameworks, test setup, 
and any existing docs like README, CONTRIBUTING, or wiki files. 
 
Then create a CLAUDE.md file in the repo root that describes: 
- Our tech stack and frameworks 
- Our coding standards and naming conventions 
- Our project structure with a folder tree 
- Our testing approach (framework, naming, patterns) 
- What you should never do in this repo 
 
Write it so that any future Claude Code session will immediately understand 
how our team works. 
 

 

For Business Analysts 

Write a ticket from a vague request 

I have a vague requirement: "[paste the vague request here]" 
 
Read the relevant code in our codebase, then write a complete work item with: 
- A clear, specific title 
- User story format: As a [role], I want [goal], so that [benefit] 
- Acceptance criteria (specific and testable) 
- Edge cases (at least 3) 
- Technical notes referencing actual code files 
- Test scenarios mapped to each acceptance criterion 
 

Break an epic into sprint-ready tickets 

Here's an epic: "[paste epic description]" 
 
Read the relevant areas of our codebase, then break this into sprint-ready work items. 
Each ticket should have: title, user story, acceptance criteria, edge cases, technical notes, 
estimated complexity (S/M/L), and dependencies on other tickets. 
Order them by implementation sequence. 
 

Write a feature spec / PRD 

I need a feature spec for: "[describe the feature]" 
 
Read the relevant code to understand our current architecture, then write a PRD with: 
- Problem statement (what's broken or missing) 
- Proposed solution (how we'll fix or build it) 
- User stories with acceptance criteria 
- Technical approach (affected files, APIs, data models) 
- Out of scope (what this does NOT include) 
- Success metrics (how we know it worked) 
 

Validate requirements against code 

Here are the requirements for a feature: "[paste requirements]" 
 
Read the codebase and tell me: 
- Which requirements are already partially implemented 
- Which ones conflict with the current architecture 
- What's missing from the requirements that a developer would need to know 
- Suggest improvements to make the requirements more precise 
 

 

For Developers 

Debug an error 

I'm getting this error: [paste error message or stack trace] 
 
Read the relevant code files, trace the execution path, explain what's going wrong, 
write a fix, and generate a test to prevent regression. 
 

Write a new feature 

I need to implement: "[describe the feature]" 
 
Read the existing codebase to understand our architecture and patterns, then: 
1. Propose an approach (which files to create/modify) 
2. Write the implementation following our existing patterns 
3. Write unit tests for all new public methods 
4. Update any relevant documentation 
 

Refactor existing code 

Read [file or folder path] and refactor it to: 
- Follow SOLID principles 
- Extract methods longer than 30 lines 
- Add proper error handling 
- Improve naming for clarity 
- Add missing documentation comments 
 
Show me the before/after for each change and explain why it's better. 
Keep all existing tests passing. 
 

Code review a file 

Review [file path] against best practices. Check for: 
- SOLID violations 
- Missing null checks or error handling 
- Async/await correctness 
- Potential performance issues (N+1 queries, memory leaks) 
- Security concerns (SQL injection, XSS, hardcoded secrets) 
- Missing tests 
- Naming and readability issues 
Suggest specific fixes with code examples. 
 

Generate tests for existing code 

Read [file or folder path] and generate comprehensive tests. 
Follow our existing test patterns and framework. 
Include: 
- Happy path tests 
- Edge cases (boundary values, empty collections, null inputs) 
- Error scenarios (invalid input, exceptions, timeouts) 
- Use parameterised tests where multiple inputs test the same behaviour 
 

Fix a failing test 

This test is failing: [paste test name or file] 
 
The error is: [paste error output] 
 
Read the test and the source code it's testing. 
Explain why it's failing and fix either the test or the source code 
(whichever is actually wrong). Don't just make the test pass — 
make sure the behaviour is correct. 
 

 

For QA Engineers 

Generate a test plan from a ticket 

Here's a work item / user story: "[paste ticket]" 
 
Read the relevant code, then create a test plan with: 
- Test scenarios mapped to each acceptance criterion 
- Edge cases the developer might have missed 
- Negative tests (what should NOT happen) 
- Data requirements (what test data is needed) 
- Environment considerations (what needs to be configured) 
Prioritise by risk: high-risk scenarios first. 
 

Write automated tests from manual test cases 

Here are our manual test cases: "[paste test cases]" 
 
Read the codebase, find the relevant code, and convert these into 
automated tests using our existing test framework and patterns. 
Include setup/teardown, test data creation, and assertions 
that match the expected outcomes from the manual tests. 
 

Generate regression tests for a change 

This PR/commit changes: "[describe what changed or paste the diff]" 
 
Read the affected code and generate regression tests that: 
- Cover all modified code paths 
- Test boundary conditions introduced by the change 
- Verify existing functionality still works 
- Include both positive and negative scenarios 
 

Review test coverage 

Read [file or folder path] and our existing tests. 
Identify: 
- Public methods with no tests 
- Code paths not covered (error handlers, edge cases, null checks) 
- Tests that exist but don't assert meaningful behaviour 
- Suggest specific tests to fill each gap 
Prioritise by risk — what would hurt most if it broke? 
 

 

For Everyone 

Generate documentation 

Read [file or folder path] and generate documentation including: 
- Purpose and responsibility of each class/module 
- Public API surface with parameter descriptions 
- Usage examples 
- Dependencies and integration points 
Write it in a format that matches our existing documentation style. 
 

Explain how something works 

I need to understand how [feature/module/process] works in our codebase. 
 
Read the relevant code and explain: 
- What it does (in plain English) 
- How the data flows through the system 
- Which files are involved 
- What external services it depends on 
- What could go wrong and how errors are handled 
Assume I'm not familiar with this part of the codebase. 
 

Find where something is implemented 

Where in our codebase is [feature/behaviour/logic] implemented? 
 
Search the code and show me: 
- The main files responsible 
- The entry point (where execution starts) 
- The data flow (how it moves through the system) 
- Any configuration that affects it 
 

 

Plan Mode vs Auto Execute 

Claude Code has two modes — you choose the level of control: 

 

Plan Mode 

Auto Execute 

How it works 

Claude proposes a plan, you approve before it acts 

Claude reads, writes, and runs immediately 

Speed 

Slower (you review each step) 

Fastest (no approval between actions) 

Best for 

Large refactors, architecture changes, unfamiliar code, high-risk work 

Bug fixes, test generation, docs, small well-understood changes 

Trust level 

"Show me before you touch anything" 

"I trust you, just do it" 

Tip: Start in Plan Mode while you're learning. Switch to Auto Execute as you build confidence. 

To use plan mode, type shift+tab to toggle between modes, or type: 

/plan [describe what you want] 
 

 

Power User: Worktrees (Parallel Agents) 

Run multiple Claude Code agents simultaneously, each in an isolated copy of your repo: 

# Start Claude Code with a worktree (isolated copy) 
claude --worktree 
 
# Or use the short flag 
claude -w 
 

Each agent gets its own branch, its own working copy, no conflicts. When it's done, review and merge. Like having 3 developers working in parallel without merge hell. 

 

Power User: Skills & Commands 

What's the difference? 

Skill = A markdown file that teaches Claude Code HOW to do something (the knowledge) 

Command = A shortcut you type to TRIGGER a workflow (the trigger) 

Create a custom skill 

Paste this into Claude Code: 

Create a skill for our team that: 
- Name: [e.g., "ticket-writer", "code-reviewer", "test-generator"] 
- Purpose: [what should it do] 
- Standards: [our specific rules, templates, or patterns it should follow] 
 
Write the SKILL.md file and save it so it's available in future sessions. 
 

Available slash commands 

Command 

What It Does 

/review-pr 

Review a pull request 

/write-spec 

Generate a feature spec from an idea 

/debug 

Investigate an error with codebase context 

/test 

Generate tests for a module 

/document 

Create documentation 

 

Quick Reference 

I want to... 

Paste this... 

Fix a bug 

I'm getting this error: [error]. Find the cause and fix it. 

Write a ticket 

Turn this into a work item: "[vague request]" 

Generate tests 

Write tests for [file]. Include edge cases. 

Review code 

Review [file] for issues and suggest fixes. 

Understand code 

Explain how [feature] works in our codebase. 

Break down an epic 

Break this epic into sprint-ready tickets: "[epic]" 

Create docs 

Document [file/folder] with examples. 

Start a new feature 

Implement [feature] following our existing patterns. 

 

Security at a Glance 

Anthropic does not train models on your code 

SOC 2 Type II certified 

Enterprise: SSO, RBAC, audit logging, SIEM integration 

Encryption: TLS 1.2+ in transit, AES-256 at rest 

Full details: trust.anthropic.com 

 

Created for the "Claude Code in Action" presentation by WeBuyCars. Questions? MarnusC@webuycars.co.za 

 