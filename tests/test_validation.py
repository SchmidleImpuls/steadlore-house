import pytest

from steadlore_house.validation import ValidationError, reject_secret_fields


def test_rejects_raw_secret_fields() -> None:
    with pytest.raises(ValidationError):
        reject_secret_fields({"service": {"password": "not-allowed"}})


def test_allows_secret_references_without_secret_material() -> None:
    reject_secret_fields(
        {
            "secret_references": [
                {
                    "label": "Home Assistant admin access",
                    "system": "1Password",
                    "vault": "Household Shared",
                    "item": "Home Assistant",
                }
            ]
        }
    )
