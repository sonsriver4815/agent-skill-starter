from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import (
    SkillStarterError,
    audit_skill,
    create_skill,
    list_examples,
    validate_skill,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skill-starter",
        description="Create, validate, and ship Agent Skills in minutes.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a new Agent Skill folder.")
    init_parser.add_argument("name", help="Skill name, e.g. repo-review-check.")
    init_parser.add_argument(
        "--path",
        default=".",
        help="Parent directory where the skill folder will be created.",
    )
    init_parser.add_argument(
        "--template",
        choices=["minimal", "workflow", "tooling"],
        default="minimal",
        help="Template to use.",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files in the target folder.",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate a Skill folder.")
    validate_parser.add_argument("path", help="Path to a skill folder or SKILL.md file.")

    audit_parser = subparsers.add_parser("audit", help="Score Skill quality heuristics.")
    audit_parser.add_argument("path", help="Path to a skill folder or SKILL.md file.")
    audit_parser.add_argument("--json", action="store_true", help="Print JSON output.")

    subparsers.add_parser("examples", help="List bundled example Skills.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            result = create_skill(
                name=args.name,
                parent=Path(args.path),
                template=args.template,
                force=args.force,
            )
            print(f"Created {result}")
            return 0

        if args.command == "validate":
            report = validate_skill(Path(args.path))
            for message in report.messages:
                print(message)
            return 0 if report.ok else 1

        if args.command == "audit":
            report = audit_skill(Path(args.path))
            if args.json:
                print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
            else:
                print(f"Score: {report.score}/100")
                for finding in report.findings:
                    if finding.deduction:
                        print(f"- [{finding.code}] {finding.title} (-{finding.deduction})")
                    else:
                        print(f"- [{finding.code}] {finding.title}")
                    print(f"  {finding.message}")
                    print(f"  Why: {finding.impact}")
                    print(f"  Fix: {finding.remediation}")
            return 0

        if args.command == "examples":
            for example in list_examples():
                print(example)
            return 0

    except SkillStarterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
