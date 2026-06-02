from __future__ import annotations

import json

from agent_skill_starter.cli import main


def test_init_validate_and_audit(tmp_path, capsys):
    assert main(["init", "demo-skill", "--template", "tooling", "--path", str(tmp_path)]) == 0

    skill_path = tmp_path / "demo-skill"
    assert (skill_path / "SKILL.md").exists()
    assert (skill_path / "agents" / "openai.yaml").exists()
    assert (skill_path / "references" / "usage.md").exists()
    assert (skill_path / "scripts").exists()

    assert main(["validate", str(skill_path)]) == 0
    assert "OK" in capsys.readouterr().out

    assert main(["audit", str(skill_path), "--json"]) == 0
    output = capsys.readouterr().out
    report = json.loads(output)
    assert report["score"] >= 80


def test_validate_rejects_missing_frontmatter(tmp_path, capsys):
    skill_path = tmp_path / "bad-skill"
    skill_path.mkdir()
    (skill_path / "SKILL.md").write_text("# Bad Skill\n", encoding="utf-8")

    assert main(["validate", str(skill_path)]) == 1
    assert "frontmatter" in capsys.readouterr().out


def test_validate_rejects_invalid_name(tmp_path, capsys):
    skill_path = tmp_path / "bad-name"
    skill_path.mkdir()
    (skill_path / "SKILL.md").write_text(
        "---\nname: Bad_Name\ndescription: Use this skill when testing invalid names in a sample skill.\n---\n\n# Bad\n",
        encoding="utf-8",
    )

    assert main(["validate", str(skill_path)]) == 1
    assert "Invalid name" in capsys.readouterr().out


def test_validate_rejects_missing_description(tmp_path, capsys):
    skill_path = tmp_path / "missing-description"
    skill_path.mkdir()
    (skill_path / "SKILL.md").write_text(
        "---\nname: missing-description\n---\n\n# Missing Description\n",
        encoding="utf-8",
    )

    assert main(["validate", str(skill_path)]) == 1
    assert "description" in capsys.readouterr().out


def test_validate_rejects_missing_reference(tmp_path, capsys):
    skill_path = tmp_path / "missing-reference"
    skill_path.mkdir()
    (skill_path / "SKILL.md").write_text(
        "---\nname: missing-reference\ndescription: Use this skill when testing missing reference links in a sample skill.\n---\n\n# Missing Reference\n\nSee [Usage](references/usage.md).\n",
        encoding="utf-8",
    )

    assert main(["validate", str(skill_path)]) == 1
    assert "Missing referenced file" in capsys.readouterr().out


def test_examples_lists_bundled_examples(capsys):
    assert main(["examples"]) == 0
    output = capsys.readouterr().out
    assert "repo-review-check" in output
    assert "local-dev-setup" in output
    assert "meeting-notes-actions" in output
