---
name: bug-reproduction
description: Use this skill when the user asks to reproduce a bug, verify a reported failure, reduce an issue to a minimal case, or capture reliable steps before fixing.
---

# Bug Reproduction

Use this skill to turn a vague bug report into a repeatable failure.

## First Checks

- Identify the reported behavior, expected behavior, affected version, and environment.
- Read the smallest relevant code path, logs, test, issue, or stack trace.
- Separate confirmed facts from guesses.
- Avoid fixing the bug until reproduction is clear.

## Workflow

- Try the narrowest command or UI path that could reproduce the failure.
- Record exact inputs, flags, files, data, and observed output.
- Reduce the scenario until only the failing condition remains.
- If reproduction fails, list what was tried and what evidence is still missing.

## Verification

- Prefer a failing test, command, fixture, or manual checklist that another agent can rerun.
- Confirm the failure still occurs after reducing the case.
- Do not mark the bug reproduced from an unrelated error.

## Final Report

- Reproduction status.
- Exact steps or command.
- Expected result.
- Actual result.
- Smallest known failing case.
- Evidence still missing, if any.
