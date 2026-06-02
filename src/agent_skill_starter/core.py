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
class AuditReport:
    score: int
    findings: list[str]

    def to_dict(self) -> dict[str, object]:
        return {"score": self.score, "findings": self.findings}


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
        return AuditReport(0, ["SKILL.md is missing valid frontmatter."])

    metadata, markdown = parsed
    description = metadata.get("description", "").strip()
    findings: list[str] = []
    score = 100

    if len(description.split()) < 16:
        score -= 20
        findings.append("Description should include richer trigger context.")

    trigger_terms = ["use when", "when", "mentions", "tasks", "work with", "for"]
    if not any(term in description.lower() for term in trigger_terms):
        score -= 20
        findings.append("Description should say when the skill should trigger.")

    body_lines = [line for line in markdown.splitlines() if line.strip()]
    if len(body_lines) > 180:
        score -= 15
        findings.append("Body is long; move details into references/ for progressive disclosure.")

    if "references/" in markdown:
        missing = [
            link
            for link in REFERENCE_LINK_RE.findall(markdown)
            if not (skill_file.parent / link).exists()
        ]
        if missing:
            score -= 20
            findings.append(f"Missing reference files: {', '.join(missing)}")

    if "## Verification" not in markdown:
        score -= 10
        findings.append("Add a Verification section.")

    if "## Final" not in markdown and "## Final Report" not in markdown:
        score -= 5
        findings.append("Add final reporting guidance.")

    if not findings:
        findings.append("Looks ready to ship.")

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
