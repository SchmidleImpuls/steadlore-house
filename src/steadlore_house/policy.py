from __future__ import annotations

from dataclasses import dataclass

from .models import ActionClass


ACTION_CLASS_RANK: dict[ActionClass, int] = {
    "safe": 0,
    "privileged": 1,
    "high_friction": 2,
    "forbidden": 3,
}

SECRET_EXPOSURE_TERMS = {
    "ask for",
    "ask the user for",
    "copy",
    "enter",
    "paste",
    "provide",
    "read out",
    "share",
    "show",
    "tell me",
    "type",
}

SECRET_MATERIAL_TERMS = {
    "api key",
    "backup code",
    "backup codes",
    "credential export",
    "password",
    "private key",
    "recovery key",
    "secret",
    "totp seed",
    "token",
}

FORBIDDEN_ACTION_TERMS = {
    "credential export",
    "delete backup",
    "delete backups",
    "delete configuration",
    "delete config",
    "delete container",
    "delete containers",
    "delete volume",
    "delete volumes",
    "remove backup",
    "remove backups",
    "remove configuration",
    "remove config",
    "remove container",
    "remove containers",
    "remove volume",
    "remove volumes",
}

HIGH_FRICTION_ACTION_TERMS = {
    "admin access",
    "backup deletion",
    "change dns",
    "change firewall",
    "change identity provider",
    "change password manager",
    "change tailscale acl",
    "change vlan",
    "dns setting",
    "dns settings",
    "firewall rule",
    "firewall rules",
    "gateway",
    "identity provider",
    "password-manager",
    "password manager",
    "switch acl",
    "tailscale acl",
    "vlan",
    "wi-fi access point",
    "wifi access point",
}

PRIVILEGED_ACTION_TERMS = {
    "change setting",
    "change settings",
    "reboot",
    "redeploy",
    "reset",
    "restart",
    "restore backup",
    "rollback",
    "ssh",
    "stop container",
    "update software",
    "upgrade",
}

SAFE_OBSERVATION_TERMS = {
    "check",
    "confirm",
    "look",
    "observe",
    "open",
    "try",
    "verify",
    "view",
}


@dataclass(frozen=True)
class PolicyDecision:
    """Deterministic policy classification for guidance text."""

    action_class: ActionClass
    reason: str
    matched_term: str | None = None


POLICY_DEFINITIONS: tuple[tuple[ActionClass, str], ...] = (
    ("safe", "Read-only or low-risk observations a Stress User may perform without special approval."),
    ("privileged", "Changes to services, containers, hosts, software, or configuration requiring explicit approval."),
    ("high_friction", "Privileged changes to core infrastructure, identity, secrets, backups, or access that could cause lockout."),
    ("forbidden", "Actions that expose secrets, delete critical data, or create unacceptable safety or lockout risk."),
)


def classify_action(text: str) -> PolicyDecision:
    """Classify action guidance using deterministic v0 policy rules.

    The classifier is intentionally conservative. It is not an authority to act;
    it is a guardrail for generated guidance and future interfaces.
    """
    lowered = " ".join(text.lower().replace("_", " ").replace("-", " ").split())

    secret_material = _first_match(lowered, SECRET_MATERIAL_TERMS)
    secret_exposure = _first_match(lowered, SECRET_EXPOSURE_TERMS)
    if secret_material and secret_exposure:
        return PolicyDecision("forbidden", "asks to expose secret material", secret_material)

    match = _first_match(lowered, FORBIDDEN_ACTION_TERMS)
    if match:
        return PolicyDecision("forbidden", "mentions destructive deletion", match)

    match = _first_match(lowered, HIGH_FRICTION_ACTION_TERMS)
    if match:
        return PolicyDecision("high_friction", "affects core infrastructure, identity, secrets, backups, or access", match)

    match = _first_match(lowered, PRIVILEGED_ACTION_TERMS)
    if match:
        return PolicyDecision("privileged", "changes service, host, software, or configuration state", match)

    match = _first_match(lowered, SAFE_OBSERVATION_TERMS)
    if match:
        return PolicyDecision("safe", "appears to be a read-only or low-risk observation", match)

    return PolicyDecision("safe", "no privileged, high-friction, or forbidden policy terms matched")


def is_stricter_or_equal(declared: ActionClass, inferred: ActionClass) -> bool:
    return ACTION_CLASS_RANK[declared] >= ACTION_CLASS_RANK[inferred]


def _first_match(text: str, terms: set[str]) -> str | None:
    for term in sorted(terms):
        normalized = " ".join(term.lower().replace("_", " ").replace("-", " ").split())
        if normalized in text:
            return term
    return None
