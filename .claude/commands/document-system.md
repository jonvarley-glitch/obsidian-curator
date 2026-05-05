---
description: Create or update a system note from the current note's content
---

# Document System

Create or update a `system` note for the technology / product / integration described in the current note.

Steps:

1. **Identify** — work out the canonical name (`Vendor Product` Title Case, e.g. `Salesforce Sales Cloud`, `Snowflake`, `Okta`).
2. **Locate or create** — check `04-Knowledge/` for an existing system note with that name. If found, update; if not, create a new one based on `Templates/system.md`.
3. **Fill the template** — populate `vendor`, `category`, `owner`, `status`, and `customer` (if customer-specific). Body sections: Purpose, Architecture, Data Flows, Integrations, APIs / Endpoints, Owners & Contacts, Notes.
4. **Architecture diagram** — keep the `![[<Title> - Architecture.excalidraw]]` embed placeholder. Tell the user to create the matching Excalidraw drawing once via Command Palette -> "Excalidraw: Create new drawing".
5. **Wikilinks** — link to related customers, projects, and other systems with `[[...]]` so the new note plugs into the graph.

Rules:

- Only include facts the source supports. Mark unknowns as "TBC" rather than guessing.
- Do not fabricate diagrams, endpoints, or owner names.
- After writing, summarise: file path, fields populated, fields left blank, links added.
