from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

EvidenceStatus = Literal["known", "unknown", "inferred", "manually_confirmed", "discovered"]
ActionClass = Literal["safe", "privileged", "high_friction", "forbidden"]


@dataclass(frozen=True)
class Evidence:
    source: str
    last_verified: str
    freshness_days: int
    status: EvidenceStatus = "known"
    confidence: str = "medium"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Evidence":
        return cls(
            source=data["source"],
            last_verified=data["last_verified"],
            freshness_days=int(data["freshness_days"]),
            status=data.get("status", "known"),
            confidence=data.get("confidence", "medium"),
        )


@dataclass(frozen=True)
class Fact:
    text: str
    evidence: Evidence

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Fact":
        return cls(text=data["text"], evidence=Evidence.from_dict(data["evidence"]))


@dataclass(frozen=True)
class SecretReference:
    label: str
    system: str
    vault: str | None = None
    item: str | None = None
    physical_hint: str | None = None
    responsible_person: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SecretReference":
        return cls(
            label=data["label"],
            system=data["system"],
            vault=data.get("vault"),
            item=data.get("item"),
            physical_hint=data.get("physical_hint"),
            responsible_person=data.get("responsible_person"),
        )


@dataclass(frozen=True)
class Person:
    id: str
    name: str
    role: str
    contact_hint: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Person":
        return cls(id=data["id"], name=data["name"], role=data["role"], contact_hint=data.get("contact_hint"))


@dataclass(frozen=True)
class Device:
    id: str
    name: str
    device_type: str
    location: str
    household_impact: str
    facts: list[Fact] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Device":
        return cls(
            id=data["id"],
            name=data["name"],
            device_type=data["device_type"],
            location=data["location"],
            household_impact=data["household_impact"],
            facts=[Fact.from_dict(item) for item in data.get("facts", [])],
        )


@dataclass(frozen=True)
class AccessEndpoint:
    label: str
    url: str
    evidence: Evidence

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AccessEndpoint":
        return cls(label=data["label"], url=data["url"], evidence=Evidence.from_dict(data["evidence"]))


@dataclass(frozen=True)
class Service:
    id: str
    name: str
    critical: bool
    plain_description: str
    household_impact: str
    depends_on: list[str] = field(default_factory=list)
    access_endpoints: list[AccessEndpoint] = field(default_factory=list)
    facts: list[Fact] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Service":
        return cls(
            id=data["id"],
            name=data["name"],
            critical=bool(data.get("critical", False)),
            plain_description=data.get("plain_description", "No plain-English description has been recorded."),
            household_impact=data["household_impact"],
            depends_on=list(data.get("depends_on", [])),
            access_endpoints=[AccessEndpoint.from_dict(item) for item in data.get("access_endpoints", [])],
            facts=[Fact.from_dict(item) for item in data.get("facts", [])],
        )


@dataclass(frozen=True)
class Inventory:
    household_name: str
    generated_for: str
    people: list[Person]
    devices: list[Device]
    services: list[Service]
    secret_references: list[SecretReference]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Inventory":
        return cls(
            household_name=data["household_name"],
            generated_for=data.get("generated_for", "trusted people and operators"),
            people=[Person.from_dict(item) for item in data.get("people", [])],
            devices=[Device.from_dict(item) for item in data.get("devices", [])],
            services=[Service.from_dict(item) for item in data.get("services", [])],
            secret_references=[SecretReference.from_dict(item) for item in data.get("secret_references", [])],
        )


@dataclass(frozen=True)
class GuidedAction:
    text: str
    action_class: ActionClass

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GuidedAction":
        return cls(text=data["text"], action_class=data["action_class"])


@dataclass(frozen=True)
class Runbook:
    id: str
    symptom: str
    applies_to: list[str]
    plain_summary: str
    probably_still_ok: list[str]
    temporary_workarounds: list[str]
    helper_note: str
    household_impact: str
    first_checks: list[GuidedAction]
    escalation_path: list[str]
    do_not_touch: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Runbook":
        return cls(
            id=data["id"],
            symptom=data["symptom"],
            applies_to=list(data.get("applies_to", [])),
            plain_summary=data["plain_summary"],
            probably_still_ok=list(data.get("probably_still_ok", [])),
            temporary_workarounds=list(data.get("temporary_workarounds", [])),
            helper_note=data.get("helper_note", ""),
            household_impact=data["household_impact"],
            first_checks=[GuidedAction.from_dict(item) for item in data.get("first_checks", [])],
            escalation_path=list(data.get("escalation_path", [])),
            do_not_touch=list(data.get("do_not_touch", [])),
        )
