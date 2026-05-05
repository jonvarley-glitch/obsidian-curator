---
description: Triage every note in 00-Inbox/ -- classify, frontmatter, rename, file
---

# Triage Inbox

Read every note in `00-Inbox/` (the user will run this from inside the Obsidian vault, not the vault-forge project). For each note:

1. **Classify** — read the content and determine the correct `type` from the vault's note types: `customer`, `person`, `meeting`, `project`, `knowledge`, `system`, `industry`, `competition`, `demo`, `partner`, `workshop`, `certification`, `daily`, `weekly-review`. Refer to `Conventions.md` if unsure.
2. **Add frontmatter** — emit `type`, `status`, and any relationship fields (`customer`, `project`, `date`) the content supports. Use wikilinks for relationships. Match the YAML key order in the existing templates.
3. **Rename** — apply the file naming convention from `Conventions.md`: dated notes use `YYYY-MM-DD - Title.md`; evergreen notes use `Title Case.md`.
4. **Move** — file the note into the matching folder (`01-Customers/`, `02-Projects/`, `03-Meetings/`, etc.). Never leave anything in `00-Inbox/` unless you genuinely cannot classify it; if so, add a TODO comment at the top explaining why.

Rules:

- Never delete content. Polish wording but preserve every fact.
- Use `[[wikilinks]]` for any customer, person, or project name in body text.
- After processing, summarise: number triaged, breakdown by type, any items left in inbox with reason.
- Do not touch notes that already live in their target folder; only those still in `00-Inbox/`.
