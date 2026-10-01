from pathlib import Path
from skill_cli.validate import validate


def test_valid_skill(tmp_path):
    d = tmp_path / "s"
    d.mkdir()
    (d / "SKILL.md").write_text("# Skill\n\n## Description\nTest.\n\n## Usage\nRun.\n")
    (d / "scripts").mkdir()
    (d / "references").mkdir()
    assert validate(d).ok


def test_missing_skill_md(tmp_path):
    assert not validate(tmp_path).ok


def test_warnings(tmp_path):
    d = tmp_path / "s"
    d.mkdir()
    (d / "SKILL.md").write_text("# Minimal\n")
    r = validate(d)
    assert r.ok
    assert len(r.warnings) > 0
