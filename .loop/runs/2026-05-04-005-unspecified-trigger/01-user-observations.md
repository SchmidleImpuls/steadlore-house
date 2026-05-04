# User Observations

## User stance
Representing the Operator as the primary setup and maintenance user, with a secondary Stress User lens for the generated Continuity Manual. Because the run trigger is unspecified, these observations are exploratory and should not be treated as a selected product slice.

## What I tried or inspected
- Read loop context: `.loop/runs/2026-05-04-005-unspecified-trigger/00-context.md`.
- Read target-user and product framing: `docs/product/TARGET_USERS.md`, `docs/product/VISION.md`, `docs/product/UBIQUITOUS_LANGUAGE.md`.
- Inspected first-use documentation in `README.md`.
- Ran CLI help:
  - `python -m steadlore_house.cli --help`
  - `python -m steadlore_house.cli generate-manual --help`
  - `python -m steadlore_house.cli discover-network --help`
  - `python -m steadlore_house.cli review-inventory-draft --help`
- Generated example outputs to `/tmp/steadlore-user-pass/`:
  - `python -m steadlore_house.cli generate-manual --inventory examples/household.yaml --runbooks examples/runbooks --output /tmp/steadlore-user-pass/manual.md`
  - `python -m steadlore_house.cli generate-ai-packet --inventory examples/household.yaml --runbooks examples/runbooks --output /tmp/steadlore-user-pass/ai.md`
  - `python -m steadlore_house.cli generate-manual --inventory examples/household.yaml --output /tmp/steadlore-user-pass/manual-no-runbooks.md`
- Inspected existing generated artifacts:
  - `dist/continuity-manual.md`
  - `dist/network-snapshot.md`
  - `dist/inventory-draft.yaml`
  - `examples/household.yaml`
  - `examples/runbooks/lights-or-automations-not-working.yaml`

## Frictions
- The Operator first-use path is still CLI-heavy. The README is clear for contributors, but an infrequent Operator would likely need to re-learn commands, paths, and the distinction between discovery snapshot, draft, reviewed Manual Inventory, runbooks, and generated manual.
- The Stress User manual starts well, but it still exposes product/internal terms early: “deterministic policy rules,” “Stress User,” “Privileged,” and “High Friction.” These are accurate but may feel more system-facing than calm household-facing language under pressure.
- The manual says “choose the closest symptom,” but the current example has only one symptom. That is acceptable for v0, but in a real household the Stress User may not know what to do when their symptom is not listed.
- `dist/network-snapshot.md` and `dist/inventory-draft.yaml` include “Possible Connector Candidates,” “connector candidates,” or `connector_hints` even though README says there is no Home Assistant, Portainer, Telegram, or other connector yet. As an Operator, this could imply an integration path that does not actually exist.
- The generated manual uses evidence and staleness well in the Helper Person section, but the Stress User section only says a dashboard link was “last checked 14 days ago.” It does not explicitly translate whether that is current, stale, or uncertain at the point of use.
- `pytest -q` failed because `pytest` is not installed in the environment. This is not a product UX failure, but it affects contributor confidence when trying to validate the runnable prototype from a fresh environment.

## Desires
- As an Operator, I would want a guided “what do I do next?” path after generating discovery output: review these candidates, confirm these fields, then generate the manual.
- As an Operator, I would want connector-related wording to disappear unless there is an actual Available Connector I can use.
- As a Stress User, I would want the manual’s first page to stay symptom-first and avoid internal product vocabulary unless needed.
- As a Stress User, I would want an explicit fallback when my problem is not in the symptom list: what is safe to check, what not to touch, and who to contact.
- As a Helper Person, I would want the dependency graph and evidence exactly as provided, but with any stale/current state easy to scan.

## Delight or value
- The generated Continuity Manual already delivers the core promise for the first scenario: it explains household impact, what is probably still okay, safe checks, what not to touch, and escalation without exposing secrets.
- The Home Assistant scenario feels aligned with the Stress User: “Internet and Wi-Fi are not necessarily affected” and “Physical wall switches may still work” are calming and useful.
- The CLI help is explicit about local-first and safety boundaries. `discover-network --help` clearly says passive discovery does not perform port scans, login attempts, cloud lookups, or inventory mutation.
- The Manual Inventory Draft clearly marks itself as draft-only and review-required, which supports the principle that discovery observations are not household meaning.
- Secret References in `examples/household.yaml` and the generated manual point to 1Password items without storing secrets.

## Evidence
- `README.md` states the project is unreleased and has no released Docker image, web interface, Telegram bot, Home Assistant connector, Portainer connector, or automated recovery workflow.
- CLI help output lists four commands: `generate-manual`, `generate-ai-packet`, `discover-network`, and `review-inventory-draft`.
- Example manual generation succeeded and wrote `/tmp/steadlore-user-pass/manual.md` and `/tmp/steadlore-user-pass/ai.md`.
- `dist/continuity-manual.md` includes the first symptom, safe checks, do-not-touch guidance, Helper Person notes, a Mermaid dependency graph, and stale/current evidence labels.
- `dist/network-snapshot.md` includes: “Possible Connector Candidates” and “Possible connector candidates: example connector candidate.”
- `dist/inventory-draft.yaml` includes `connector_hints` and a fact saying “Possible connector candidate for 192.0.2.1: example connector candidate.”
- `python -m steadlore_house.cli generate-manual --inventory examples/household.yaml --output /tmp/steadlore-user-pass/manual-no-runbooks.md` succeeded and produced a clear “No runbooks have been added yet” message.
- `pytest -q` returned `/usr/bin/bash: line 1: pytest: command not found`.

## Suggested next improvements
1. Remove or hide connector-candidate language from user-facing discovery and draft outputs until there is a real Available Connector.
2. Add a calmer fallback section for unlisted symptoms in the Continuity Manual’s “Start Here” area.
3. Soften Stress User-facing policy wording while preserving exact policy definitions in a Helper Person or Operator section.
4. Make staleness more explicit in Stress User-facing useful links, e.g. whether “last checked 14 days ago” is current, stale, or close to stale.
5. Add a concise Operator workflow guide that connects discovery snapshot → Manual Inventory Draft → review → generated Continuity Manual.
6. Consider making the README test command use the project’s dev install path explicitly, since `pytest` may not exist in a fresh environment until `python -m pip install -e .[dev]` is run.

## Non-blocking caveats
- This is persona simulation based on repository artifacts, not direct observation of a real Operator, Stress User, or Helper Person.
- The run trigger was empty, so the observations should inform selection only if the human wants this loop to discover a small next increment from current strategy.
- I did not run live network discovery to avoid unnecessary environmental variation; I inspected the existing deterministic `dist/network-snapshot.md` instead.
