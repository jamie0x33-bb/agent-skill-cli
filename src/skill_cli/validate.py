"""Skill directory validation against the Agent Skills spec."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationResult:
    ok: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


REQUIRED = ["SKILL.md"]
RECOMMENDED = ["scripts", "references"]


def validate(skill_dir: Path) -> ValidationResult:
    result = ValidationResult()

    if not skill_dir.is_dir():
        result.ok = False
        result.errors.append(f"not a directory: {skill_dir}")
        return result

    for name in REQUIRED:
        if not (skill_dir / name).exists():
            result.ok = False
            result.errors.append(f"missing required: {name}")

    for name in RECOMMENDED:
        if not (skill_dir / name).is_dir():
            result.warnings.append(f"recommended directory missing: {name}/")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.is_file():
        content = skill_md.read_text()
        if not content.startswith("#"):
            result.warnings.append("SKILL.md should start with a heading")
        for section in ("Description", "Usage"):
            if f"## {section}" not in content:
                result.warnings.append(f"SKILL.md missing section: {section}")

    return result
