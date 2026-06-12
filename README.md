# agent-skill-starter

Build reusable `SKILL.md` folders for coding agents.

[![Tests](https://github.com/sonsriver4815/agent-skill-starter/actions/workflows/tests.yml/badge.svg)](https://github.com/sonsriver4815/agent-skill-starter/actions/workflows/tests.yml)

`agent-skill-starter` is a small CLI for turning repeated agent workflows into reusable `SKILL.md` folders.

Use it when a prompt, checklist, review process, or tool setup keeps coming up and deserves a stable home.

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

PyPI publishing is being prepared. After the first package release, installation will be:

```bash
pipx install agent-skill-starter
```

## What is an Agent Skill?

An Agent Skill is a small folder that tells a coding agent how to do one recurring job well.

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

Each finding includes:

- what failed
- why it matters
- how to fix it
- the score deduction

JSON output uses the same structure, so scripts can read `code`, `impact`, `remediation`, and `deduction` directly.

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

Different agents discover and load skills differently. This project keeps the output plain so you can copy it where your agent expects it.

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

Build the package locally:

```bash
python -m build
```

## PyPI publishing status

PyPI publishing is prepared but not enabled yet.

The repository includes a GitHub Actions workflow for PyPI Trusted Publishing. Before using it, configure a PyPI Trusted Publisher for this repository:

- repository: `sonsriver4815/agent-skill-starter`
- workflow: `publish.yml`
- environment: `pypi`

After that is configured on PyPI, publish a GitHub Release to upload the package.

Exit codes:

- `0`: success
- `1`: validation error
- `2`: usage error

## Roadmap

- finish PyPI Trusted Publisher setup
- add more real-world skill examples
- explain audit scoring in more detail
- add a `copy-example` command

## GitHub topics

`ai-agents`, `codex`, `claude-code`, `agent-skills`, `developer-tools`, `cli`

## License

MIT
