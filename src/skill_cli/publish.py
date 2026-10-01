"""Publish a skill to the registry.

Validates the skill directory, builds the archive, and registers it with
the configured registry endpoint. Requires an authenticated session —
see ``config.load_auth()`` for the credential resolution chain.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path

from . import __version__
from .config import load
from .validate import validate


def publish(skill_dir: Path, dry_run: bool = False) -> dict:
    """Publish a skill to the registry.

    Validates the skill, then POSTs the manifest to the registry.
    In dry-run mode, validates and authenticates but does not register.
    """
    result = validate(skill_dir)
    if not result.ok:
        return {"error": "validation_failed", "errors": result.errors}

    cfg = load()
    if not cfg.authenticated:
        return {"error": "no_credential", "message": "No auth credential found in environment"}

    skill_md = (skill_dir / "SKILL.md").read_text()
    name = skill_dir.name
    title = skill_md.split("\n")[0].lstrip("# ").strip() if skill_md else name

    manifest = {
        "name": name,
        "title": title,
        "version": __version__,
        "dry_run": dry_run,
    }

    headers = {"content-type": "application/json"}
    headers.update(cfg.auth_header())

    url = f"{cfg.registry_url}/api/register"
    req = urllib.request.Request(
        url,
        data=json.dumps(manifest).encode(),
        method="POST",
        headers=headers,
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return {"error": exc.code, "body": exc.read().decode(errors="replace")[:300]}
    except urllib.error.URLError as exc:
        return {"error": str(exc)}
