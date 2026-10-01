"""Skill packaging — build a distributable archive from a skill directory."""

from __future__ import annotations

import hashlib
import json
import os
import tarfile
import tempfile
from pathlib import Path


def build(skill_dir: Path, output_dir: Path | None = None) -> Path:
    output_dir = output_dir or Path(".")
    name = skill_dir.name
    files = _collect(skill_dir)
    checksum = _checksum(skill_dir, files)

    archive = output_dir / f"{name}-{checksum[:8]}.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for relpath in files:
            tar.add(str(skill_dir / relpath), arcname=f"{name}/{relpath}")

        manifest = {
            "name": name,
            "files": files,
            "checksum": checksum,
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(manifest, f, indent=2)
            f.flush()
            tar.add(f.name, arcname=f"{name}/manifest.json")
        os.unlink(f.name)

    return archive


def _collect(skill_dir: Path) -> list[str]:
    files = []
    for root, dirs, filenames in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in filenames:
            if fname.startswith("."):
                continue
            files.append(os.path.relpath(os.path.join(root, fname), skill_dir))
    return sorted(files)


def _checksum(skill_dir: Path, files: list[str]) -> str:
    h = hashlib.sha256()
    for relpath in files:
        h.update((skill_dir / relpath).read_bytes())
    return h.hexdigest()[:16]
