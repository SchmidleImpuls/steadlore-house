# Steadlore House

**Securing continuity.**

Steadlore House is a local-first household continuity system for homes where important knowledge lives in one person’s head.

Its purpose is simple: help a household understand what depends on what, what matters most, what to do when something breaks, and where trusted people can find help without exposing secrets or making things worse.

> We have prepared for this.

## Current status

Steadlore House is not installable yet.

This repository currently contains the foundation for the project: product intent, vocabulary, architecture principles, contribution rules, and early examples.

There is no released application, Docker image, network scanner, Telegram bot, Home Assistant connector, Portainer connector, or automated recovery workflow yet.

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

**Home Assistant is unavailable after a container redeploy.**

The goal is not to let an AI freely fix the problem.

The goal is to help a trusted person understand:

- what Home Assistant is
- what household functions are affected
- whether internet and Wi-Fi still work
- what is safe to check
- what must not be touched
- who should be contacted
- where the relevant access information is stored

## Design stance

Steadlore House is not a generic chatbot, smart-home hub, password manager, monitoring dashboard, estate-planning app, or autonomous infrastructure agent.

The first useful artifact is the continuity manual.

Conversation interfaces, connectors, diagnostics, and supervised remediation may come later, but they must serve the manual and the safety model.

## For contributors

Start with:

- `AGENTS.md`
- `CONTRIBUTING.md`
- `docs/vision.md`
- `docs/ubiquitous-language.md`

The project is intentionally strict about language, safety, and scope.

If a concept cannot be explained clearly in the project vocabulary, it probably should not be implemented yet.