from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

SECRET_FIELD_NAMES = {
    "password",
    "passphrase",
    "token",
    "api_key",
    "apikey",
    "secret",
    "private_key",
    "recovery_key",
    "totp_seed",
    "backup_code",
}


class ValidationError(ValueError):
    """Raised when input data is unsafe or invalid."""


def reject_secret_fields(value: Any, *, path: str = "root") -> None:
    """Reject raw secret-looking fields in structured input.

    Secret References are allowed as explicit objects, but raw secret fields are
    not allowed in inventory, runbooks, examples, tests, or generated output.
    """
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key)
            normalized = key_text.lower().replace("-", "_")
            child_path = f"{path}.{key_text}"
            if normalized in SECRET_FIELD_NAMES:
                raise ValidationError(f"Raw secret field is not allowed: {child_path}")
            reject_secret_fields(child, path=child_path)
        return

    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        for index, child in enumerate(value):
            reject_secret_fields(child, path=f"{path}[{index}]")
