---
name: {{name}}
description: Use this skill when the user asks for {{display_name}} tooling work, including command usage, scripts, reference-backed workflows, validation, and troubleshooting.
---

# {{display_name}}

Use this skill for tooling tasks where deterministic commands or bundled references help.

## First Checks

- Read relevant local policy and project files.
- Prefer existing project commands before adding new tools.
- Avoid touching secrets, credentials, or production configuration.

## Resources

- Use `references/usage.md` for supported command patterns.
- Use scripts only when deterministic behavior is more reliable than rewriting code.

## Workflow

- Explain commands before running them.
- Keep command output focused and summarize important results.
- Ask before dependency changes, deletion, commits, pushes, or broad replacements.

## Verification

- Run the narrowest representative command.
- Validate generated files or configuration after changes.

## Final Report

- Report what changed.
- Report live verification and any remaining manual step.
