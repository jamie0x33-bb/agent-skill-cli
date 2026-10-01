from skill_cli.config import load, load_auth, fingerprint


def test_fingerprint_hides_value():
    fp = fingerprint("secret-token-value")
    assert "secret-token-value" not in fp
    assert len(fp) == 12


def test_fingerprint_none():
    assert fingerprint(None) is None


def test_load_auth_chain(monkeypatch):
    monkeypatch.delenv("SKILL_REGISTRY_TOKEN", raising=False)
    monkeypatch.delenv("PPLX_CONNECTOR_API_KEY", raising=False)
    monkeypatch.delenv("PPLX_AGENT_PROXY_TOKEN", raising=False)
    assert load_auth() is None


def test_load_auth_priority(monkeypatch):
    monkeypatch.setenv("SKILL_REGISTRY_TOKEN", "first")
    monkeypatch.setenv("PPLX_SDK_API_KEY", "second")
    assert load_auth() == "first"


def test_config_unauthenticated(monkeypatch):
    monkeypatch.delenv("SKILL_REGISTRY_TOKEN", raising=False)
    monkeypatch.delenv("PPLX_CONNECTOR_API_KEY", raising=False)
    monkeypatch.delenv("PPLX_AGENT_PROXY_TOKEN", raising=False)
    cfg = load()
    assert not cfg.authenticated
    assert cfg.auth_header() == {}
