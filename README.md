<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SchmidleImpuls/brand-assets/main/Steadlore/logo/2026-logo-steadlore-dark.svg">
  <img src="https://raw.githubusercontent.com/SchmidleImpuls/brand-assets/main/Steadlore/logo/2026-logo-steadlore-light.svg" alt="Steadlore" width="420">
</picture>

# Steadlore House

**Securing continuity.**

Steadlore House is a local-first household continuity system for homes where important knowledge lives in one person’s head.

Its purpose is simple: help a household understand what depends on what, what matters most, what to do when something breaks, and where trusted people can find help without exposing secrets or making things worse.

> We have prepared for this.

## Current status

Steadlore House is not released yet.

This repository currently contains the foundation for the project plus an initial Python prototype that can generate a passive local Network Discovery Snapshot, read example YAML, and generate a Markdown Continuity Manual and an AI Assistance Packet.

There is no released Docker image, web interface, Telegram bot, Home Assistant connector, Portainer connector, or automated recovery workflow yet. Network discovery is limited to a local snapshot and optional explicit `nmap` ping scan.

## What Steadlore House is meant to become

Steadlore House will generate and maintain a living continuity manual for household-critical infrastructure and procedures.

Examples of household-critical knowledge include:

- what each physical box is for
- which services run where
- what breaks if a device is offline
- how smart-home devices are controlled
- what to check first during an outage
- which actions are safe
- which actions require approval
- which actions are forbidden
- who can help
- where credentials or vendor information are stored

Steadlore House should never store passwords, recovery keys, TOTP seeds, or emergency-kit contents. It may store references to external secret managers, such as the vault and item name in 1Password.

## First target scenario

The first useful version will focus on one concrete failure mode:

**Lights or automations are not working.**

The goal is not to let an AI freely fix the problem.

The goal is to help a potentially stressed household member understand:

- what may be affected
- what is probably still okay
- what is safe to check
- what must not be touched
- who should be contacted
- where the relevant access information is stored

The same source data can also produce an AI Assistance Packet for a chatbot helping the household member perform safe checks only, and helper-facing technical context for a contacted helper person.

## Design stance

Steadlore House is not a generic chatbot, smart-home hub, password manager, monitoring dashboard, estate-planning app, or autonomous infrastructure agent.

The first useful artifact is the continuity manual.

Conversation interfaces, connectors, diagnostics, and supervised remediation may come later, but they must serve the manual and the safety model.

## For contributors

Start with:

- [`AGENTS.md`](AGENTS.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`docs/vision.md`](docs/vision.md)
- [`docs/ubiquitous-language.md`](docs/ubiquitous-language.md)
- [`docs/data-model.md`](docs/data-model.md)

Generate a local network snapshot with:

```bash
python -m pip install -e .[dev]
python -m steadlore_house.cli discover-network \
  --output dist/network-snapshot.md
```

You can also generate a review-required Manual Inventory draft from the curated candidates:

```bash
python -m steadlore_house.cli discover-network \
  --output dist/network-snapshot.md \
  --inventory-draft dist/inventory-draft.yaml
```

Steadlore automatically tries to enrich MAC addresses from a local `nmap-mac-prefixes` file when one is installed. You can override this with a local `nmap-mac-prefixes` or IEEE OUI file:

```bash
python -m steadlore_house.cli discover-network \
  --mac-vendors path/to/nmap-mac-prefixes \
  --output dist/network-snapshot.md
```

This reads local OS network state only. To opt into an active ping scan with an existing `nmap` installation, either let Steadlore use locally discovered IPv4 subnets:

```bash
python -m steadlore_house.cli discover-network \
  --active-scan \
  --output dist/network-snapshot.md
```

or provide one or more explicit scan targets:

```bash
python -m steadlore_house.cli discover-network \
  --active-scan \
  --subnet 192.0.2.0/24 \
  --output dist/network-snapshot.md
```

Generate the example manual outputs with:

```bash
python -m steadlore_house.cli generate-manual \
  --inventory examples/household.yaml \
  --runbooks examples/runbooks \
  --output dist/continuity-manual.md

python -m steadlore_house.cli generate-ai-packet \
  --inventory examples/household.yaml \
  --runbooks examples/runbooks \
  --output dist/ai-assistance-packet.md
```

The project is intentionally strict about language, safety, and scope.

If a concept cannot be explained clearly in the project vocabulary, it probably should not be implemented yet.

## License and brand

Steadlore House source code is licensed under the GNU Affero General Public License v3.0. See [`LICENSE`](LICENSE).

The Steadlore name, Steadlore House name, logos, wordmarks, icons, visual identity, and related brand assets are not licensed under the AGPL-3.0. The logo displayed in this README identifies the official Steadlore House project and does not grant permission to reuse Steadlore brand assets in forks, derivatives, products, services, domains, package names, marketing material, or user interfaces.

Forks and derivatives must make clear that they are unofficial and should use their own name and visual identity unless they have prior written permission.

See the [Schmidle Impuls brand assets repository](https://github.com/SchmidleImpuls/brand-assets) for brand usage rules.