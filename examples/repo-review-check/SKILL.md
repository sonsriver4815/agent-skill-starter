---
name: repo-review-check
description: Use this skill when the user asks for a focused repository review, implementation drift check, pull request sanity check, or read-only second opinion before changes.
---

# Repo Review Check

Use this skill for bounded review work where findings matter more than broad commentary.

## First Checks

- Identify the target diff, files, issue, or plan.
- Confirm review dimensions such as correctness, security, tests, or maintainability.
- Keep the review read-only unless the user explicitly asks for fixes.

## Review Rules

- Lead with actionable findings ordered by severity.
- Ground each finding in a specific file, line, behavior, or missing test.
- Avoid style-only comments unless they create real maintenance risk.
- Separate confirmed issues from assumptions.

## Verification

- Run the narrowest read-only test, lint, or static check when available.
- If checks are not available, state the review was inspection-only.

## Final Report

- Findings first.
- Open questions or assumptions second.
- Brief summary and residual risk last.
