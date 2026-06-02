# agent-skill-starter

Create, validate, and ship Agent Skills in minutes.

[![Tests](https://github.com/sonsriver4815/agent-skill-starter/actions/workflows/tests.yml/badge.svg)](https://github.com/sonsriver4815/agent-skill-starter/actions/workflows/tests.yml)

`agent-skill-starter` is a tiny CLI and template kit for building `SKILL.md`-style Agent Skills for Codex, Claude Code, OpenCode, and other coding agents that can load task-specific instructions.

It helps you move from "I keep repeating this workflow in chat" to a reusable, validated skill folder that another agent can actually use.

## 30-second quickstart

Install from a local checkout:

```bash
git clone https://github.com/sonsriver4815/agent-skill-starter.git
cd agent-skill-starter
python -m pip install -e .
skill-starter init repo-review-check --template workflow
skill-starter validate repo-review-check
skill-starter audit repo-review-check
```

When a PyPI release is available, the install command will become:

```bash
pipx install agent-skill-starter
```

Local development with tests:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
skill-starter init demo-skill --template tooling --path .
skill-starter validate demo-skill
skill-starter audit demo-skill --json
```

## Why this exists

Agent Skills are most useful when they are small, specific, and easy to trigger. In practice, many skills fail because they are too vague, too long, missing validation, or full of private project details.

This starter gives you:

- templates for common skill shapes
- validation for required `SKILL.md` structure
- audit checks for trigger quality and progressive disclosure
- examples that are safe to copy
- a lightweight CLI with no runtime dependencies

## Works with

- Codex-style `SKILL.md` folders
- Claude Code repository workflows
- OpenCode and other agents that can load task-specific markdown instructions
- Plain repository templates for teams that want reusable agent playbooks

## Why Agent Skills fail

- The description does not explain when the skill should trigger.
- The body is a long document instead of a workflow.
- Private machine paths or project-only assumptions leak into examples.
- There is no verification section, so agents stop after making changes.
- Detailed references are pasted into `SKILL.md` instead of loaded progressively.

## Before and after

Before:

```markdown
# Review stuff

Check code and tell me what is wrong.
```

After:

```markdown
---
name: repo-review-check
description: Use this skill when the user asks for a focused repository review, implementation drift check, pull request sanity check, or read-only second opinion before changes.
---

# Repo Review Check

Use this skill for bounded, read-only review work.

## First Checks

- Identify the target files, diff, issue, or plan.
- Confirm the review dimensions and maximum findings.
- Keep findings grounded in specific files and behavior.

## Verification

- Run only read-only checks unless the user asks otherwise.

## Final Report

- Lead with findings ordered by severity.
- Include test gaps and residual risk.
```

## CLI demo

```bash
skill-starter examples
skill-starter init local-dev-setup --template tooling
skill-starter validate local-dev-setup
skill-starter audit local-dev-setup
skill-starter audit local-dev-setup --json
```

Exit codes:

- `0`: success
- `1`: validation error
- `2`: usage error

## Templates

- `minimal`: creates only `SKILL.md`
- `workflow`: creates a step-by-step workflow skill
- `tooling`: creates `SKILL.md`, `references/`, and `scripts/`

## What makes a good Skill?

- The `description` says exactly when the skill should trigger.
- The body contains procedures, not generic advice.
- The skill is narrow enough to be useful.
- Private paths, tokens, customer names, and machine-specific assumptions are removed.
- Detailed reference material lives in `references/`, not the main `SKILL.md`.
- Scripts are included only when deterministic execution matters.
- Verification and final reporting are explicit.

## Compatibility

This project targets the portable `SKILL.md` folder pattern:

```text
skill-name/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
  assets/
```

Different agents expose skills differently. The generated folders are intentionally plain so they can be copied into Codex, Claude Code, OpenCode, or any repository-level agent workflow.

## Examples

Bundled examples:

- `repo-review-check`
- `local-dev-setup`
- `meeting-notes-actions`

Copy one, edit the frontmatter, then run:

```bash
skill-starter validate path/to/skill
skill-starter audit path/to/skill
```

## GitHub topics

Use these topics when publishing the repository:

`ai-agents`, `codex`, `claude-code`, `agent-skills`, `developer-tools`, `cli`

## License

MIT
