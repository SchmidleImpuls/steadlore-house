# User Observations

## User stance
Representing the Operator as the primary setup and maintenance user, while checking whether the generated Continuity Manual already serves the Stress User during the first concrete symptom: “Lights or automations are not working.”

## What I tried or inspected
- Read loop context: `.loop/runs/2026-05-04-004-first-minimal-useful-slice/00-context.md`.
- Read product docs: `docs/product/TARGET_USERS.md`, `docs/product/VISION.md`, and `docs/product/UBIQUITOUS_LANGUAGE.md`.
- Inspected CLI entry points and help:
  - `python -m steadlore_house.cli --help`
  - `python -m steadlore_house.cli generate-manual --help`
- Generated example outputs:
  - `python -m steadlore_house.cli generate-manual --inventory examples/household.yaml --runbooks examples/runbooks --output /tmp/steadlore-continuity-manual.md`
  - `python -m steadlore_house.cli generate-ai-packet --inventory examples/household.yaml --runbooks examples/runbooks --output /tmp/steadlore-ai-assistance-packet.md`
  - `python -m steadlore_house.cli discover-network --output /tmp/steadlore-network-snapshot.md --inventory-draft /tmp/steadlore-inventory-draft.yaml`
- Inspected existing example/source artifacts:
  - `examples/household.yaml`
  - `examples/runbooks/lights-or-automations-not-working.yaml`
  - `dist/continuity-manual.md`
  - `dist/network-snapshot.md`
  - `dist/inventory-draft.yaml`
- Ran tests with `python -m pytest -q`.

## Frictions
- As an Operator, the example YAML is still the main setup surface. It is understandable, but not yet a “first useful slice” for someone who will only touch this rarely.
- The generated Continuity Manual is useful for the Stress User, but it does not yet clearly show a dependency graph in the manual. `examples/household.yaml` says Home Assistant `depends_on` `house-server-01`, but the generated manual mainly surfaces that relationship indirectly through Helper Person evidence.
- The CLI help is clear for contributors, but a household Operator may still need a more obvious “start here” path: discover, review, generate manual, then inspect gaps.
- The passive Network Discovery Snapshot is honest that candidates are not trusted Manual Inventory, but the next step from “candidate” to “reviewed household meaning” still feels high-friction and CLI-heavy.
- There is no released Docker image, web UI, or Operator-facing Infrastructure Map yet, per `README.md`, so the first experience remains prototype/developer-oriented.

## Desires
- I want the generated manual to include a small, visible dependency view for the Home Assistant scenario: Home Assistant → House Server 01, with stale/known/unknown markers.
- I want a minimal Operator review artifact that shows what Steadlore knows, what it discovered, what is stale, and what still needs human review.
- I want the first-run path to say: “Generate this example, then replace these fields with your household,” without making me infer the workflow from several commands.
- I want Stress User guidance to stay symptom-first, but I want Helper Person appendices to expose enough technical structure to reduce guessing.

## Delight or value
- The generated Continuity Manual already feels aligned with the product promise. It starts from the symptom, explains household impact, lists what is probably still okay, gives safe checks, and says what not to touch.
- The Home Assistant example is concrete and calm: it avoids implying that internet or Wi-Fi are broken, and it suggests physical wall switches as a workaround.
- Secret handling is reassuring. The manual stores Secret References only and explicitly says no passwords or recovery keys are included.
- Evidence and age are visible. The generated manual marks stale facts, including the House Server fact, and the AI Assistance Packet tells a chatbot not to invent missing facts.
- The discovery snapshot correctly labels itself observational and not trusted Manual Inventory until reviewed.
- Tests pass locally with `python -m pytest -q` (`59 passed in 0.17s`).

## Evidence
- `README.md` states the project can generate a passive local Network Discovery Snapshot, read example YAML, and generate a Markdown Continuity Manual and AI Assistance Packet; it also states there is no released Docker image, web interface, Telegram bot, Home Assistant connector, Portainer connector, or automated recovery workflow yet.
- `examples/household.yaml` includes `depends_on: house-server-01` for Home Assistant.
- Generated `/tmp/steadlore-continuity-manual.md` includes:
  - “Common symptoms: Lights or automations are not working”
  - safe checks such as trying a physical wall switch and checking ordinary internet browsing
  - do-not-touch guidance for gateway, switches, Wi-Fi access points, containers, volumes, backups, firewall, DNS, VLAN, identity-provider, and password-manager settings
  - Secret Reference locations without secrets
  - stale evidence markers for facts whose freshness windows have expired
- Generated `/tmp/steadlore-ai-assistance-packet.md` includes chatbot instructions to use only packet facts, treat stale facts as possibly outdated, avoid asking for secrets, and avoid privileged/high-friction first checks.
- `dist/network-snapshot.md` includes a Mermaid network map and clearly says the snapshot is observational, incomplete, and requires review before becoming Manual Inventory.
- CLI commands completed successfully for manual generation, AI packet generation, and passive discovery. Tests passed with `python -m pytest -q`.

## Suggested next improvements
1. Add the smallest dependency graph rendering to the Continuity Manual and/or Helper Person appendix for the existing Home Assistant example.
2. Add a minimal Markdown Infrastructure Map that shows reviewed Manual Inventory, discovered candidates, stale facts, unknowns/gaps, and dependencies without introducing a GUI.
3. Improve first-run documentation around one complete Operator path: generate example → run passive discovery → review draft → generate Continuity Manual.
4. Make the Manual Inventory draft review path easier to rehearse with example data, so Operators understand promotion before running it on their own household.
5. Add explicit “unknowns/gaps” to the generated Continuity Manual so the Stress User and Helper Person can see what Steadlore does not know.

## Non-blocking caveats
- This is persona simulation based on repository artifacts, generated Markdown, and CLI behavior, not direct testing with a real Operator, Stress User, or Helper Person.
- I did not inspect a GUI or screenshots because none appear to exist in the current runnable product.
- I generated a live passive discovery snapshot only to verify the command path; I did not rely on or quote local machine/network details as product evidence.
