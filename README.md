# agent-skill-starter

Create, validate, and ship Agent Skills in minutes.

[![Tests](https://github.com/sonsriver4815/agent-skill-starter/actions/workflows/tests.yml/badge.svg)](https://github.com/sonsriver4815/agent-skill-starter/actions/workflows/tests.yml)

`agent-skill-starter` is a small CLI for creating `SKILL.md` folders that coding agents can reuse.

Use it when you have a repeated agent workflow, prompt, checklist, review process, or tool setup that should become a reusable Agent Skill instead of staying buried in chat history.

## What you get

- `skill-starter init`: generate a new skill folder from a template
- `skill-starter validate`: catch broken `SKILL.md` frontmatter and missing references
- `skill-starter audit`: score whether a skill is clear enough for agents to trigger and use
- starter templates for minimal, workflow, and tooling skills
- copyable examples for reviews, local setup, and meeting notes

## Quickstart

Clone the repo and install it locally:

```bash
git clone https://github.com/sonsriver4815/agent-skill-starter.git
cd agent-skill-starter
python -m pip install -e .
```

Create and check your first skill:

```bash
skill-starter init repo-review-check --template workflow
skill-starter validate repo-review-check
skill-starter audit repo-review-check
```

Example output:

```text
Created repo-review-check
OK
Score: 100/100
- Looks ready to ship.
```

PyPI publishing is not set up yet. After the first package release, installation will be:

```bash
pipx install agent-skill-starter
```

## What is an Agent Skill?

An Agent Skill is a small folder that tells an AI coding agent how to do one recurring job well.

```text
repo-review-check/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

The most important file is `SKILL.md`. It contains:

- frontmatter that tells the agent when to use the skill
- short workflow instructions
- verification rules
- final reporting guidance

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

## Commands

### `init`

Create a new skill folder.

```bash
skill-starter init local-dev-setup --template tooling
```

Templates:

- `minimal`: only `SKILL.md`
- `workflow`: step-by-step workflow skill
- `tooling`: `SKILL.md`, `references/`, and `scripts/`

### `validate`

Check required structure.

```bash
skill-starter validate local-dev-setup
```

It checks:

- valid YAML-style frontmatter
- required `name`
- required `description`
- lowercase hyphenated skill name
- missing files linked from `references/`

### `audit`

Score whether a skill is easy for an agent to trigger and use.

```bash
skill-starter audit local-dev-setup
skill-starter audit local-dev-setup --json
```

It looks for:

- trigger-friendly descriptions
- overly long `SKILL.md` bodies
- missing verification guidance
- missing final reporting guidance
- broken reference links

### `examples`

List bundled example skills.

```bash
skill-starter examples
```

Bundled examples:

- `repo-review-check`
- `local-dev-setup`
- `meeting-notes-actions`

## Works with

This project uses plain folders and markdown so the output can be copied into different agent workflows:

- Codex-style `SKILL.md` folders
- Claude Code repository workflows
- OpenCode and similar coding agents
- team repositories that keep reusable agent playbooks

Different agents discover and load skills differently. This project focuses on creating clean, portable skill folders.

## What makes a good Skill?

- The `description` says exactly when the skill should trigger.
- The body is a workflow, not a long essay.
- The skill handles one recurring job.
- Private paths, tokens, customer names, and machine-specific assumptions are removed.
- Detailed reference material lives in `references/`.
- Scripts are included only when deterministic execution matters.
- Verification and final reporting are explicit.

## Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e . -r requirements-dev.txt
python -m pytest -q
```

Exit codes:

- `0`: success
- `1`: validation error
- `2`: usage error

## Roadmap

- publish to PyPI
- add more real-world skill examples
- explain audit scoring in more detail
- add a `copy-example` command

## GitHub topics

`ai-agents`, `codex`, `claude-code`, `agent-skills`, `developer-tools`, `cli`

## License

MIT
