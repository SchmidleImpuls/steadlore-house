from steadlore_house.policy import classify_action, is_stricter_or_equal


def test_classifies_safe_observations() -> None:
    decision = classify_action("Check whether ordinary internet browsing works.")

    assert decision.action_class == "safe"


def test_classifies_container_restart_as_privileged() -> None:
    decision = classify_action("Restart the Home Assistant container.")

    assert decision.action_class == "privileged"


def test_classifies_core_infrastructure_changes_as_high_friction() -> None:
    assert classify_action("Change DNS settings.").action_class == "high_friction"
    assert classify_action("Change firewall rules.").action_class == "high_friction"
    assert classify_action("Change VLAN settings.").action_class == "high_friction"


def test_classifies_destructive_or_secret_exposing_actions_as_forbidden() -> None:
    assert classify_action("Delete backups for this service.").action_class == "forbidden"
    assert classify_action("Remove volumes used by the container.").action_class == "forbidden"
    assert classify_action("Ask the user for a password or recovery key.").action_class == "forbidden"


def test_declared_action_class_must_be_at_least_as_strict_as_inferred_policy() -> None:
    assert is_stricter_or_equal("high_friction", "privileged")
    assert not is_stricter_or_equal("safe", "privileged")
