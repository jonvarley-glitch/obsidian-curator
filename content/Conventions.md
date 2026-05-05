# Vault Conventions

This guide documents the naming, tagging, and metadata rules for this vault. Consistent conventions are critical for Dataview queries, AI retrieval (RAG), and long-term maintainability.

## Note Types

Every note must have a `type` frontmatter property. Valid values:

`customer` | `person` | `meeting` | `project` | `knowledge` | `system` | `industry` | `competition` | `demo` | `partner` | `workshop` | `certification` | `daily` | `weekly-review`

The `system` type documents a specific technology, product, or integration. Name systems in Title Case with the `Vendor Product` pattern (e.g. `Salesforce Sales Cloud.md`, `Snowflake.md`, `Okta.md`). System notes live in `04-Knowledge/` and are filtered by `type = "system"`.

## Status Values

Where applicable, notes have a `status` property. Valid values:

`active` | `inactive` | `completed` | `archived` | `draft`

Status is always a frontmatter property, never a tag.

## File Naming

- **Evergreen notes**: Title Case with spaces. Example: `Acme Corp.md`, `Architecture Overview.md`
- **Dated notes**: `YYYY-MM-DD - Title.md`. Example: `2026-03-09 - Weekly Sync with Acme Corp.md`
- **Avoid**: `# | ^ : % [[ ]]` in filenames

## Folder Naming

- Numbered hyphenated prefixes: `01-Customers`, `02-Projects`
- Title Case after prefix
- Utility folders have no prefix: `Templates`, `Prompts`, `Assets`
- Maximum 3 levels of nesting

## Frontmatter Rules

- **Relationship fields use wikilinks**: `customer: "[[Acme Corp]]"` -- creates backlinks and enables Dataview queries
- **No blank properties**: If a field doesn't apply, omit it entirely
- **Dates**: ISO 8601 format `YYYY-MM-DD`
- **Aliases**: YAML list format for customers and people:
  ```yaml
  aliases:
    - Acme
    - ACME Corp
  ```

## Tags

Tags are for cross-cutting themes that span note types and folders. Define your own taxonomy and apply it consistently.

Rules:
- Never duplicate what frontmatter captures (no `#meeting`, no `#acme`)
- Flat namespace only (no nested tags like `#parent/child`)
- No status tags

## Links

- Use wikilinks: `[[Acme Corp]]`, `[[Sarah Chen]]`, `[[Q1 Migration Project]]`
- Links are the primary organisational tool -- they build the knowledge graph
- Shortest path format (no folder paths in links)

## Headings

- H1 is the note title (matches filename)
- Body sections start at H2
- Never skip heading levels

## Diagrams

**Excalidraw is the default diagramming tool.** Drawings live in `Assets/Excalidraw/`. Name them `<Note Title> - <Diagram Topic>.excalidraw` so they sort logically and embed predictably:

```markdown
![[Acme Corp - High-Level Architecture.excalidraw]]
```

Use Excalidraw for: architecture diagrams, C4 context/container/component, sequence flows you want to redraw freely, whiteboard sessions, workshop captures.

**Use Mermaid only for trivial inline diagrams** where Excalidraw would be overkill — for example a five-line sequence diagram inside a meeting or project note. Fenced as ```` ```mermaid ```` blocks.

## Bases vs Dataview

- **Dataview** for inline tables on hub pages (Home, customer, project notes).
- **Bases** for standalone interactive views in the `Bases/` folder.

Both ship with the vault. Pick whichever fits the situation.

## Decisions Log

Project-level decisions live inline in project notes under a **Decisions Log** H2, each as an H3:

```markdown
### 2026-03-09 - Adopt Snowflake over BigQuery

- **Context:** ...
- **Options considered:** ...
- **Decision:** ...
- **Consequences:** ...
```

The H3 date pattern keeps decisions searchable across the vault without a dedicated note type. Use the `decision-matrix` Copilot prompt to draft one quickly.

## Maintenance Cadence

- **Weekly**: File or discard `00-Inbox/` notes. Run weekly review.
- **Monthly**: Run Find Orphaned Files. Check for broken links. Review archive.
- **Quarterly**: Audit customer statuses. Review tag taxonomy. Check for stale projects.
