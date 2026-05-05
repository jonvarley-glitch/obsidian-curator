---
type: prompt
title: System Documentation
---

Create or update a `system` note for the technology / product / integration described in the current note.

Use the `system` template structure and fill in:

1. **Frontmatter**: `type: system`, `vendor`, `category`, `owner`, `status`, and `customer` if the system is customer-specific.
2. **Purpose** — one paragraph: what it does and why it exists in this architecture.
3. **Architecture** — keep the `![[<Title> - Architecture.excalidraw]]` embed placeholder; do not invent a Mermaid diagram unless the source clearly describes one.
4. **Data Flows** — inbound and outbound, refresh cadence, volume if known.
5. **Integrations** — fill the table with any connected systems mentioned (direction, protocol, notes).
6. **APIs / Endpoints** — list any URLs, endpoints, or named APIs.
7. **Owners & Contacts** — names, roles, responsibilities.
8. **Notes** — anything else from the source that doesn't fit elsewhere.

Rules:

- Only include facts the source supports. Mark unknowns explicitly (e.g. "TBC: refresh cadence").
- Use wikilinks for related customers, projects, and other systems: `[[Snowflake]]`, `[[Acme Corp]]`.
- Place the resulting note in `04-Knowledge/`.
- File name: `Vendor Product.md` in Title Case (e.g. `Salesforce Sales Cloud.md`, `Snowflake.md`).
