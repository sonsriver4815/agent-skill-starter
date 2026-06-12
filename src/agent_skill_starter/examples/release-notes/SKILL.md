---
name: release-notes
description: Use this skill when the user asks to draft release notes, summarize shipped changes, prepare a changelog entry, or turn commits into reader-facing update notes.
---

# Release Notes

Use this skill to write concise release notes from real changes.

## First Checks

- Identify the release version, date, audience, and source of truth.
- Read the relevant commits, pull requests, issues, changelog, or diff.
- Separate shipped changes from planned work.
- Do not invent metrics, dates, or compatibility guarantees.

## Workflow

- Group changes by user-facing outcome, not by internal file order.
- Call out breaking changes, migration steps, and known limitations first.
- Keep implementation details only when they help users understand impact.
- Link issues or pull requests when available.

## Verification

- Check each note against a source commit, issue, PR, or changed file.
- Confirm version numbers and dates match the release.
- Verify that known limitations are not hidden in generic wording.

## Final Report

- Release title and summary.
- Added, changed, fixed, and removed items where applicable.
- Breaking changes or migration notes.
- Source gaps or unverified claims.
