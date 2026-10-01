"""Runtime configuration and credential resolution.

Auth credentials are resolved from the first available source:

1. ``SKILL_REGISTRY_TOKEN`` — explicit registry credential
2. ``PPLX_SDK_API_KEY`` — SDK credential
3. ``PPLX_CONNECTOR_API_KEY`` — connector-scoped key

The resolved credential is sent as an ``x-api-key`` header for registry
operations.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass

REGISTRY_URL = os.environ.get(
    "SKILL_REGISTRY_URL", "https://skill-publish-api.vercel.app"
)

AUTH_CHAIN = [
    "SKILL_REGISTRY_TOKEN",
    "PPLX_SDK_API_KEY",
    "PPLX_CONNECTOR_API_KEY",
]


@dataclass(frozen=True)
class Config:
    registry_url: str
    auth_token: str | None
    agent_id: str | None

    @property
    def authenticated(self) -> bool:
        return self.auth_token is not None

    def auth_header(self) -> dict[str, str]:
        if not self.auth_token:
            return {}
        return {"x-api-key": self.auth_token}


def load_auth() -> str | None:
    for var in AUTH_CHAIN:
        val = os.environ.get(var)
        if val:
            return val
    return None


def load() -> Config:
    return Config(
        registry_url=REGISTRY_URL,
        auth_token=load_auth(),
        agent_id=os.environ.get("ASI_EXTERNAL_TOOLS_AGENT_ID"),
    )


def fingerprint(value: str | None) -> str | None:
    if not value:
        return None
    return hashlib.sha256(value.encode()).hexdigest()[:12]
