---
name: local-dev-setup
description: Use this skill when the user asks to inspect, install, verify, or troubleshoot a local developer environment, CLI tool, plugin, shell path, or project startup workflow.
---

# Local Dev Setup

Use this skill for local setup work that must end with live verification.

## Safety Defaults

- Explain commands before running them.
- Do not touch secrets, tokens, production config, or credentials.
- Ask before dependency changes, file deletion, commits, pushes, or broad rewrites.
- Prefer project-defined setup, test, lint, and start commands.

## Discovery

- Read local instructions before changing configuration.
- Check whether the requested tool is already installed.
- Verify the command that actually wins on `PATH`.
- Distinguish missing tools from shell, sandbox, or permission failures.

## Workflow

- Make the smallest setup change that can satisfy the request.
- Prefer user-level configuration only when the task is cross-project.
- Keep output focused and summarize the important result.

## Verification

- Run the installed command's version or health check.
- Run one representative harmless command when functional verification is needed.

## Final Report

- Report what changed.
- Report what was verified live.
- Note any restart or manual step that remains.
