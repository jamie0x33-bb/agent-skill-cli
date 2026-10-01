import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from skill_cli.publish import publish


def _make_skill(tmp_path):
    d = tmp_path / "test-skill"
    d.mkdir()
    (d / "SKILL.md").write_text("# Test Skill\n\n## Description\nA test.\n\n## Usage\nRun.\n")
    (d / "scripts").mkdir()
    return d


def test_publish_dry_run(tmp_path, monkeypatch):
    monkeypatch.setenv("SKILL_REGISTRY_TOKEN", "test-token")
    skill = _make_skill(tmp_path)

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"registered": True, "publish_id": "pub-test"}).encode()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
        result = publish(skill, dry_run=True)

    assert result["registered"] is True
    call_req = mock_open.call_args[0][0]
    assert call_req.get_header("X-api-key") == "test-token"


def test_publish_no_auth(tmp_path, monkeypatch):
    from skill_cli.config import AUTH_CHAIN
    for var in AUTH_CHAIN:
        monkeypatch.delenv(var, raising=False)
    skill = _make_skill(tmp_path)
    result = publish(skill)
    assert result["error"] == "no_credential"


def test_publish_invalid_skill(tmp_path, monkeypatch):
    monkeypatch.setenv("SKILL_REGISTRY_TOKEN", "test-token")
    result = publish(tmp_path)
    assert result["error"] == "validation_failed"
