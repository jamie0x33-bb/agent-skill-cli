from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, config, validate, build


def _validate(args) -> int:
    result = validate.validate(Path(args.directory))
    for e in result.errors:
        print(f"error:   {e}")
    for w in result.warnings:
        print(f"warning: {w}")
    print("valid" if result.ok else "invalid")
    return 0 if result.ok else 1


def _build(args) -> int:
    skill_dir = Path(args.directory)
    output = Path(args.output) if args.output else None
    archive = build.build(skill_dir, output)
    print(f"built {archive}")
    return 0


def _auth(args) -> int:
    cfg = config.load()
    if args.token:
        if cfg.authenticated:
            print(cfg.auth_token)
        else:
            print("no auth credential found", file=sys.stderr)
            return 1
    else:
        print(f"authenticated: {cfg.authenticated}")
        if cfg.authenticated:
            print(f"fingerprint:   {config.fingerprint(cfg.auth_token)}")
        print(f"registry:      {cfg.registry_url}")
    return 0


def _info(args) -> int:
    cfg = config.load()
    info = {
        "version": __version__,
        "registry": cfg.registry_url,
        "authenticated": cfg.authenticated,
        "credential_fingerprint": config.fingerprint(cfg.auth_token),
        "agent_id": cfg.agent_id,
    }
    print(json.dumps(info, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="skill-cli", description="Perplexity Computer skill CLI")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="validate a skill directory")
    v.add_argument("directory")
    v.set_defaults(func=_validate)

    b = sub.add_parser("build", help="build a skill archive")
    b.add_argument("directory")
    b.add_argument("-o", "--output", metavar="DIR")
    b.set_defaults(func=_build)

    a = sub.add_parser("auth", help="check auth status")
    a.add_argument("--token", action="store_true", help="print the raw token")
    a.set_defaults(func=_auth)

    i = sub.add_parser("info", help="environment info")
    i.set_defaults(func=_info)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
