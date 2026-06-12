from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from importlib import resources
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n(?P<markdown>.*)\Z", re.DOTALL)
REFERENCE_LINK_RE = re.compile(r"\]\((references/[^)]+)\)")


class SkillStarterError(Exception):
    """Expected CLI error."""


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    messages: list[str]


@dataclass(frozen=True)
class AuditFinding:
    code: str
    title: str
    message: str
    impact: str
    remediation: str
    deduction: int

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "title": self.title,
            "message": self.message,
            "impact": self.impact,
            "remediation": self.remediation,
            "deduction": self.deduction,
        }


@dataclass(frozen=True)
class AuditReport:
    score: int
    findings: list[AuditFinding]

    def to_dict(self) -> dict[str, object]:
        return {
            "score": self.score,
            "findings": [finding.to_dict() for finding in self.findings],
        }


def create_skill(name: str, parent: Path, template: str, force: bool = False) -> Path:
    if not NAME_RE.match(name):
        raise SkillStarterError(
            "skill name must use lowercase letters, digits, and hyphens only"
        )
    template_root = _resource_path("templates") / template
    if not template_root.exists():
        raise SkillStarterError(f"unknown template: {template}")

    target = parent / name
    if target.exists() and not force:
        raise SkillStarterError(f"{target} already exists; pass --force to overwrite")
    target.mkdir(parents=True, exist_ok=True)

    for source in template_root.rglob("*"):
        relative = source.relative_to(template_root)
        destination = target / relative
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        text = source.read_text(encoding="utf-8")
        destination.write_text(_render_template(text, name), encoding="utf-8")

    return target


def validate_skill(path: Path) -> ValidationReport:
    skill_file = _resolve_skill_file(path)
    messages: list[str] = []
    parsed = _parse_skill(skill_file)

    if parsed is None:
        return ValidationReport(False, ["SKILL.md must start with YAML frontmatter."])

    metadata, markdown = parsed
    name = metadata.get("name", "").strip()
    description = metadata.get("description", "").strip()

    if not name:
        messages.append("Missing required frontmatter field: name")
    elif not NAME_RE.match(name):
        messages.append("Invalid name: use lowercase letters, digits, and hyphens only")

    if not description:
        messages.append("Missing required frontmatter field: description")
    elif len(description.split()) < 8:
        messages.append("Description is too short to trigger reliably")

    if not markdown.strip():
        messages.append("SKILL.md body is empty")

    for link in REFERENCE_LINK_RE.findall(markdown):
        reference_path = skill_file.parent / link
        if not reference_path.exists():
            messages.append(f"Missing referenced file: {link}")

    if not messages:
        messages.append("OK")
    return ValidationReport(messages == ["OK"], messages)


def audit_skill(path: Path) -> AuditReport:
    skill_file = _resolve_skill_file(path)
    parsed = _parse_skill(skill_file)
    if parsed is None:
        return AuditReport(
            0,
            [
                AuditFinding(
                    code="frontmatter-missing",
                    title="Missing frontmatter",
                    message="SKILL.md is missing valid frontmatter.",
                    impact="Agents cannot discover the skill name or trigger description reliably.",
                    remediation="Start SKILL.md with YAML frontmatter containing name and description.",
                    deduction=100,
                )
            ],
        )

    metadata, markdown = parsed
    description = metadata.get("description", "").strip()
    findings: list[AuditFinding] = []
    score = 100

    if len(description.split()) < 16:
        deduction = 20
        score -= deduction
        findings.append(
            AuditFinding(
                code="description-too-short",
                title="Description is too short",
                message="Description should include richer trigger context.",
                impact="Short descriptions are easy to miss because agents only see metadata before loading the skill body.",
                remediation="Mention the task type, concrete triggers, and at least one boundary for when to use the skill.",
                deduction=deduction,
            )
        )

    trigger_terms = ["use when", "when", "mentions", "tasks", "work with", "for"]
    if not any(term in description.lower() for term in trigger_terms):
        deduction = 20
        score -= deduction
        findings.append(
            AuditFinding(
                code="trigger-context-missing",
                title="Trigger context is missing",
                message="Description should say when the skill should trigger.",
                impact="Agents may ignore the skill or use it for unrelated requests.",
                remediation="Add wording such as 'Use when...' followed by the user requests or files that should trigger the skill.",
                deduction=deduction,
            )
        )

    body_lines = [line for line in markdown.splitlines() if line.strip()]
    if len(body_lines) > 180:
        deduction = 15
        score -= deduction
        findings.append(
            AuditFinding(
                code="body-too-long",
                title="Skill body is long",
                message="Body is long; move details into references/ for progressive disclosure.",
                impact="Large skill bodies consume context before the agent knows which details matter.",
                remediation="Keep SKILL.md focused on the workflow and move examples, schemas, and variants into references/.",
                deduction=deduction,
            )
        )

    if "references/" in markdown:
        missing = [
            link
            for link in REFERENCE_LINK_RE.findall(markdown)
            if not (skill_file.parent / link).exists()
        ]
        if missing:
            deduction = 20
            score -= deduction
            findings.append(
                AuditFinding(
                    code="reference-missing",
                    title="Referenced file is missing",
                    message=f"Missing reference files: {', '.join(missing)}",
                    impact="Agents will follow broken instructions and lose the detailed context the skill promised.",
                    remediation="Create the missing reference file or remove the stale link from SKILL.md.",
                    deduction=deduction,
                )
            )

    if "## Verification" not in markdown:
        deduction = 10
        score -= deduction
        findings.append(
            AuditFinding(
                code="verification-missing",
                title="Verification guidance is missing",
                message="Add a Verification section.",
                impact="Agents may stop after editing without proving the skill worked.",
                remediation="Add '## Verification' with the closest test, lint, dry run, or manual check expected for this task.",
                deduction=deduction,
            )
        )

    if "## Final" not in markdown and "## Final Report" not in markdown:
        deduction = 5
        score -= deduction
        findings.append(
            AuditFinding(
                code="final-report-missing",
                title="Final reporting guidance is missing",
                message="Add final reporting guidance.",
                impact="Different agents may finish with inconsistent summaries or omit verification results.",
                remediation="Add '## Final Report' with the exact fields the agent should report back.",
                deduction=deduction,
            )
        )

    if not findings:
        findings.append(
            AuditFinding(
                code="ready",
                title="Looks ready to ship",
                message="Looks ready to ship.",
                impact="No structural audit issues were found.",
                remediation="Use the skill on a real task and revise it from execution evidence.",
                deduction=0,
            )
        )

    return AuditReport(max(score, 0), findings)


def list_examples() -> list[str]:
    root = _resource_path("examples")
    return sorted(path.name for path in root.iterdir() if path.is_dir())


def _resolve_skill_file(path: Path) -> Path:
    if path.is_dir():
        path = path / "SKILL.md"
    if not path.exists():
        raise SkillStarterError(f"not found: {path}")
    if path.name != "SKILL.md":
        raise SkillStarterError("path must be a skill folder or SKILL.md")
    return path


def _parse_skill(path: Path) -> tuple[dict[str, str], str] | None:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    metadata: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, match.group("markdown")


def _render_template(text: str, name: str) -> str:
    display_name = name.replace("-", " ").title()
    return text.replace("{{name}}", name).replace("{{display_name}}", display_name)


def _resource_path(name: str) -> Path:
    packaged = Path(str(resources.files("agent_skill_starter") / name))
    if packaged.exists():
        return packaged
    project_root = Path(__file__).resolve().parents[2]
    fallback = project_root / name
    if fallback.exists():
        return fallback
    return packaged
