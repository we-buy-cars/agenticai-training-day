# Claude Skills

## 1. Create a Skills Folder

In your project root, create something like:

```
/claude-skills/
```

or if you're using agent frameworks:

```
/.claude/skills/
```

## 2. Create a Skill File

Most setups use YAML or JSON.

**Example: `refactor-code.yaml`**

```yaml
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
```

## 3. Register / Load the Skill

Once the skill file is saved, it becomes available in future Claude Code sessions within your project.
