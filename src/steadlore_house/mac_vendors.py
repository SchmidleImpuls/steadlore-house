from __future__ import annotations

import shutil
from pathlib import Path


VENDOR_CONNECTOR_HINTS: tuple[tuple[str, str], ...] = (
    ("ubiquiti", "UniFi connector candidate"),
    ("raspberry pi", "host/device inventory candidate"),
    ("synology", "NAS connector candidate"),
    ("qnap", "NAS connector candidate"),
    ("shelly", "smart-home device candidate"),
    ("espressif", "smart-home / IoT candidate"),
    ("signify", "Hue/Home Assistant connector candidate"),
    ("philips lighting", "Hue/Home Assistant connector candidate"),
    ("sonos", "Sonos household service candidate"),
    ("apple", "client or smart-home device candidate; low confidence"),
    ("google", "client or smart-home device candidate; low confidence"),
    ("amazon", "client or smart-home device candidate; low confidence"),
)


def normalize_mac_prefix(value: str | None) -> str | None:
    if not value:
        return None
    hex_chars = "".join(char for char in value.upper() if char in "0123456789ABCDEF")
    if len(hex_chars) < 6:
        return None
    if set(hex_chars[:6]) in [{"0"}, {"F"}]:
        return None
    return hex_chars[:6]


class MacVendorLookup:
    def __init__(self, vendors_by_prefix: dict[str, str] | None = None, *, source: str | None = None) -> None:
        self._vendors_by_prefix = vendors_by_prefix or {}
        self.source = source

    @property
    def is_enabled(self) -> bool:
        return bool(self._vendors_by_prefix)

    @classmethod
    def empty(cls) -> "MacVendorLookup":
        return cls({})

    @classmethod
    def from_file(cls, path: Path) -> "MacVendorLookup":
        return cls(parse_vendor_file(path.read_text(encoding="utf-8", errors="replace")), source=str(path))

    def vendor_for(self, mac_address: str | None) -> str | None:
        prefix = normalize_mac_prefix(mac_address)
        if not prefix:
            return None
        return self._vendors_by_prefix.get(prefix)

    def connector_hints_for(self, mac_address: str | None) -> tuple[str, ...]:
        return connector_hints_for_vendor(self.vendor_for(mac_address))


def connector_hints_for_vendor(vendor: str | None) -> tuple[str, ...]:
    if not vendor:
        return ()
    lowered = vendor.lower()
    return tuple(hint for term, hint in VENDOR_CONNECTOR_HINTS if term in lowered)


def discover_nmap_mac_prefixes() -> Path | None:
    candidates: list[Path] = []
    nmap_path = shutil.which("nmap")
    if nmap_path:
        binary = Path(nmap_path)
        candidates.extend(
            [
                binary.with_name("nmap-mac-prefixes"),
                binary.parent.parent / "share" / "nmap" / "nmap-mac-prefixes",
                binary.parent / "share" / "nmap" / "nmap-mac-prefixes",
            ]
        )
    candidates.extend(
        [
            Path("C:/Program Files/Nmap/nmap-mac-prefixes"),
            Path("C:/Program Files (x86)/Nmap/nmap-mac-prefixes"),
            Path("/usr/share/nmap/nmap-mac-prefixes"),
            Path("/usr/local/share/nmap/nmap-mac-prefixes"),
            Path("/opt/homebrew/share/nmap/nmap-mac-prefixes"),
        ]
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def load_mac_vendor_lookup(path: Path | None = None, *, auto_discover: bool = True) -> MacVendorLookup:
    if path:
        return MacVendorLookup.from_file(path)
    if auto_discover:
        discovered = discover_nmap_mac_prefixes()
        if discovered:
            return MacVendorLookup.from_file(discovered)
    return MacVendorLookup.empty()


def parse_vendor_file(text: str) -> dict[str, str]:
    """Parse local nmap-mac-prefixes or IEEE OUI-style files."""
    vendors: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if "(hex)" in stripped:
            prefix_part, vendor_part = stripped.split("(hex)", 1)
            prefix = normalize_mac_prefix(prefix_part)
            vendor = vendor_part.strip()
        else:
            parts = stripped.split(maxsplit=1)
            if len(parts) != 2:
                continue
            prefix = normalize_mac_prefix(parts[0])
            vendor = parts[1].strip()

        if prefix and vendor:
            vendors[prefix] = vendor
    return vendors
