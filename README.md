# agent-skill-cli

CLI for building, testing, and publishing Perplexity Computer skills.

## Install

```bash
pip install -e .
```

## Commands

```bash
skill-cli validate ./my-skill     # check skill structure
skill-cli build ./my-skill        # build a distributable archive
skill-cli auth                    # check credential status
skill-cli info                    # environment summary
```

## Auth

Credentials are resolved from the environment in priority order — see
`src/skill_cli/config.py` for the chain. `skill-cli auth` prints the
credential fingerprint without disclosing the raw value.

## Skill structure

```
my-skill/
  SKILL.md       # required
  scripts/       # recommended
  references/    # recommended
```

## Contributing

```bash
pip install -e ".[dev]"
pytest
```
